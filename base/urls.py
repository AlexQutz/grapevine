from django.urls import path
from .views import UserRegistrationAPIView, UserDetailsAPIView, PasswordResetAPIView, SkillActionAPIView

urlpatterns = [
    path('users/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('users/get/', UserDetailsAPIView.as_view(), name='user-detail-view'),
    path('users/change_password/', PasswordResetAPIView.as_view(), name = 'change-password'),
    path('users/skill/',SkillActionAPIView.as_view(),name= 'skill-action'),
]