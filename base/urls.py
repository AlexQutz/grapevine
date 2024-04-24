from django.urls import path
from .views import *

urlpatterns = [
    path('users/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('users/get/', UserDetailsAPIView.as_view(), name='user-detail-view'),
    path('users/change_password/', PasswordResetAPIView.as_view(), name = 'change-password'),
    path('users/skill/',SkillActionAPIView.as_view(),name= 'skill-action'),
    path('users/statistics/',UserStatisticsAPIView.as_view(),name='user-statistics'),
    
    path('projects/create/',CreateProjectAPIView.as_view(), name='create-project'),
    path('projects/open-seats/',ProjectsOpenSeatsAPIView.as_view(), name='open-seats-projects'),
    path('projects/interest/',ProjectInterestAPIView.as_view(), name='interests'),
    path('projects/<int:project_id>/',ProjectCompletionDeletionAPIView.as_view(), name='project-completion-deletion'),
]