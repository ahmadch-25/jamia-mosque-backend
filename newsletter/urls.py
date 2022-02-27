from django.urls import path
from .views import NewsletterView


urlpatterns = [
    path('getnewsletters/', NewsletterView.as_view()),
]