from django.urls import path,include
from .views import CampaignListView,GenratePaymentUrl, ListenWebHook, CalculateZakat


urlpatterns = [
    path('campaign/', CampaignListView.as_view()),
    path('listenwebhook/', ListenWebHook.as_view()),
    path('calculatezakat/', CalculateZakat.as_view()),
    path('genratepaymentlink/', GenratePaymentUrl.as_view())
]