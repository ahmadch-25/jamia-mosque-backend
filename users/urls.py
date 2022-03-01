from django.urls import path, include
from .views import UserLogin, UserRegister, UserUpdate, UserContributions, ChangePasswordView

urlpatterns = [
    path('users/register', UserRegister.as_view()),
    path('users/login', UserLogin.as_view()),
    path('users/update', UserUpdate.as_view()),
    path('users/change_password', ChangePasswordView.as_view()),
    path('users/contributions', UserContributions.as_view())
]
