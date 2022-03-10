from django.urls import path
from .views import SidebarListView


urlpatterns = [
    path('getsidebars/', SidebarListView.as_view()),
]