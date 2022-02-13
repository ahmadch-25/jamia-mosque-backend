from django.urls import path,include
from .views import CampaignListView,GenratePaymentUrl, ListenWebHook


urlpatterns = [
    path('campaign/', CampaignListView.as_view()),
    path('listenwebhook/', ListenWebHook.as_view()),
    path('genratepaymentlink/', GenratePaymentUrl.as_view())
]