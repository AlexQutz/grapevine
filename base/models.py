from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True)
    country = models.CharField(max_length=100, null=True)
    residence = models.CharField(max_length=100 , null=True)
    programminglanguages = models.ManyToManyField('ProgrammingLanguage', related_name='user_programming_languages', blank=True)
    
    
class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=100)    
    
class Project(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    maximum_collaborators = models.PositiveIntegerField()
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_projects')
    collaborators = models.ManyToManyField('User', related_name='projects_collaborating')
    completed = models.BooleanField(default=False)
    
class ProjectInterest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    