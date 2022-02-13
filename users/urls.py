from django.urls import path, include
from .views import UserLogin, UserRegister, UserUpdate, UserContributions

urlpatterns = [
    path('users/register', UserRegister.as_view()),
    path('users/login', UserLogin.as_view()),
    path('users/update', UserUpdate.as_view()),
    path('users/contributions', UserContributions.as_view())
]
