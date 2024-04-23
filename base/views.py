from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer , PasswordResetSerializer , SkillActionSerializer
from django.contrib.auth import get_user_model
from .models import ProgrammingLanguage

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
                    return Response({'detail': f'"{skill}" programming language added successfully with proficiency level "{expertise}".'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Maximum of 3 skills already registered.'}, status=status.HTTP_400_BAD_REQUEST)
            elif action == 'remove': 
                if user.programminglanguages.filter(name=skill, expertise=expertise).exists():
                    
                    language_to_remove = ProgrammingLanguage.objects.get(name=skill, expertise=expertise)
                    user.programminglanguages.remove(language_to_remove.id)
                    return Response({'detail': f'"{skill}" programming language removed successfully.'}, status=status.HTTP_200_OK)
                
                else:
                    return Response({'detail': f'"{skill}" in "{expertise}" level not found in user\'s skills.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    