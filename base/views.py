from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.contrib.auth import get_user_model
from .models import *
from django.db.models import Count,F


# --------------------------USER FUNCTIONALITIES-----------------------------


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({'User registered with token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        user = request.user
        serializer = UserRegistrationSerializer(user)
        return Response({'User data ': serializer.data }, status=status.HTTP_200_OK)
    
class PasswordResetAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            User = get_user_model()
            try:
                user = request.user
            except User.DoesNotExist:
                return Response({'ERROR': 'User with this username does not exist!'}, status=status.HTTP_404_NOT_FOUND)
            
            user.set_password(new_password)
            user.save()
            return Response({'Password changed successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SkillActionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request , username):
        serializer = SkillActionSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data['action']
            skill = serializer.validated_data['skill']
            expertise = serializer.validated_data['expertise']
            
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'ERROR': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            
            if action == 'add':
                
                if user.programminglanguages.filter(name=skill, expertise=expertise).exists():
                    return Response({'detail': f'"{skill}" programming language is already registered!!'}, status=status.HTTP_400_BAD_REQUEST)
                
                programming_language, created = ProgrammingLanguage.objects.get_or_create(name=skill, expertise=expertise)
                
                
                if user.programminglanguages.count() < 3:
                    user.programminglanguages.add(programming_language)
                    return Response({'detail': f"'{skill}' programming language added successfully with proficiency level '{expertise}'."}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Maximum of 3 skills already registered.'}, status=status.HTTP_400_BAD_REQUEST)
            elif action == 'remove': 
                if user.programminglanguages.filter(name=skill, expertise=expertise).exists():
                    
                    language_to_remove = ProgrammingLanguage.objects.get(name=skill, expertise=expertise)
                    user.programminglanguages.remove(language_to_remove.id)
                    return Response({'detail': f"'{skill}' programming language removed successfully."}, status=status.HTTP_200_OK)
                
                else:
                    return Response({'detail': f"'{skill}' in '{expertise}' level not found in user\'s skills."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserStatisticsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        projects_contributed = Project.objects.filter(collaborators=request.user).count()
        projects_created = Project.objects.filter(creator=request.user).count()
        
        
        statistics_data = {
            'projects_contributed': projects_contributed,
            'projects_created': projects_created,
        }
        
        
        serializer = UserStatisticsSerializer(statistics_data)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    
#--------------------------------PROJECT FUNCTIONALITIES----------------------------------------

class CreateProjectAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['creator'] = request.user
            serializer.save()
            message = f"Project with name '{serializer.validated_data['project_name']}' created by {request.user.username}."
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProjectsOpenSeatsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        open_seat_projects = Project.objects.annotate(collaborators_count=Count('collaborators')).filter(
            collaborators_count__lt=F('maximum_collaborators')).exclude(creator=request.user)
        
        serializer = ProjectSerializer(open_seat_projects, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ProjectInterestAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        project_interests = ProjectInterest.objects.filter(project__creator=request.user)
        serializer = ProjectInterestCollaboratorSerializer(project_interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        
        project_id = request.data.get('project_id')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"message": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        
        if request.user != project.creator:
            project_interest = ProjectInterest.objects.create(project=project, user=request.user)
            serializer = ProjectInterestSerializer(project_interest)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You cannot express interest in your own project."}, status=status.HTTP_400_BAD_REQUEST)
    

class ProjectCompletionDeletionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id):
        
        
        try:
            project = Project.objects.get(id=project_id, creator=request.user)
        except Project.DoesNotExist:
            return Response({"message": "Project not found or you are not the creator."}, status=status.HTTP_404_NOT_FOUND)

        
        project.completed = True
        project.save()

        return Response({"message": "Project completed successfully."}, status=status.HTTP_200_OK)

    def delete(self, request, project_id):
        
        
        try:
            project = Project.objects.get(id=project_id, creator=request.user)
        except Project.DoesNotExist:
            return Response({"message": "Project not found or you are not the creator."}, status=status.HTTP_404_NOT_FOUND)

        
        project.delete()

        return Response({"message": "Project deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    