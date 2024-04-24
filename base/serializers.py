from rest_framework import serializers
from .models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'age', 'country', 'residence', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def to_representation(self, instance):
        # Use the authenticated user instance from the request
        user = instance
        return super().to_representation(user)
    
class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, write_only=True)
    
    
class SkillActionSerializer(serializers.Serializer):
    ACTION_CHOICES = [('add', 'Add'), ('remove', 'Remove')]
    
    LANGUAGE_CHOICES = [
        ('C++', 'C++'),
        ('Javascript', 'Javascript'),
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('Lua', 'Lua'),
        ('Rust', 'Rust'),
        ('Go', 'Go'),
        ('Julia', 'Julia'),
    ]
    
    EXPERTISE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    action = serializers.ChoiceField(choices=ACTION_CHOICES)
    skill = serializers.ChoiceField(choices =LANGUAGE_CHOICES)
    expertise = serializers.ChoiceField(choices = EXPERTISE_CHOICES)
    
    
class UserStatisticsSerializer(serializers.Serializer):
    projects_contributed = serializers.IntegerField()
    projects_created = serializers.IntegerField()
    
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'maximum_collaborators', 'creator', 'collaborators']
        read_only_fields = ['id', 'creator', 'collaborators']
        
class ProjectInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInterest
        fields = ['id', 'project', 'user', 'message', 'accepted', 'created_at']
        
        
class ProjectInterestCollaboratorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    skills = serializers.ListField(child=serializers.CharField(), source='user.skills', read_only=True)

    class Meta:
        model = ProjectInterest
        fields = ['username', 'email', 'skills']