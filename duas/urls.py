from django.urls import path, include
from .views import GetAllDuas

urlpatterns = [
    path('getallduas/', GetAllDuas.as_view()),
]
