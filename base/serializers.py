from rest_framework import serializers
from .models import User,ProgrammingLanguage,Project

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
    
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'maximum_collaborators', 'creator', 'collaborators']
        read_only_fields = ['id', 'creator', 'collaborators']