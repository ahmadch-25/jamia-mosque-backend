from django.shortcuts import render, redirect
import json
from datetime import datetime

from firebase_admin import messaging
from intasend import APIService
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CampaignSerializer
from .models import DonationItems, CampaignContribution

from intasend.utils import generate_keys
from django.contrib.auth.models import User
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice

private_key = """-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwhxnB5aZD6EqF....8laHwYTQdDbAlCGZB992YoHl
    -----END PRIVATE KEY-----"""
token = "a8184850d012267e3d717491a2c99cbb3545efbbdc0bf1275291c492faff41a0"
publishable_key = "ISPubKey_test_13a61255-5b3a-4342-964e-04e49616e8c0"


class CampaignListView(APIView):

    def get(self, request):
        donations_items = DonationItems.objects.filter(publish=True)
        donations_items = CampaignSerializer(donations_items, many=True)
        print(donations_items.data)
        return Response(donations_items.data, status=status.HTTP_200_OK)


def index(request):
    device = FCMDevice.objects.all().first()
    # send_message parameters include: message, dry_run, app
    device.send_message(Message(
        data={
            "Nick": "Mario",
            "body": "great match!",
            "Room": "PortugalVSDenmark"
        },
    ))
    return render(request, "index.html")


class GenrateCheckoutLink(APIView):
    def post(self, request):
        request_data = request.data


class GenratePaymentUrl(APIView):

    def post(self, request):
        request_data = request.data
        service = APIService(token=token, publishable_key=publishable_key, private_key=private_key, test=True)
        user = User.objects.filter(email=request_data["email"]).first()
        response = service.collect.checkout(
            phone_number=request_data["phone_number"],
            email=request_data["email"], amount=request_data["amount"], currency="KES",
            comment="Fees"

            ,
            first_name=request_data["first_name"], last_name=request_data["last_name"],
            api_ref=request_data["campaign_id"] + "_" + user.id

        )
        print(response)
        return Response({"message": "success", "error": False, "url": response["url"]}, status=status.HTTP_200_OK)


class ListenWebHook(APIView):

    def post(self, request):
        request_data = request.data
        if request_data["state"] == "COMPLETE":
            api_info = request_data["api_ref"].split("_")
            user = User.objects.get(pk=api_info[1])
            campaign = DonationItems.objects.get(pk=api_info[0])
            campaign.contribution_amount += int(float(request_data["value"]))
            campaign.save()
            donation_contributtion = CampaignContribution(user=user, campaign=campaign,
                                                          amount=int(float(request_data["value"])))
            fcm_device = FCMDevice.objects.filter(user=user).first()
            fcm_device.send_message(Message(
                notification=Notification(title="Payment Received",
                                          body="Your payment for Donation is Completed, Thank you",
                                          image="https://cdn3.iconfinder.com/data/icons/fintech-43/32/FINTECH_RAW_-_FILLED_FLAT-05-512.png"),
            ))
            donation_contributtion.save()
        return Response({"message": "success", "error": False})

    def get(self, request):
        print("get")
        request_data = request.data
        print(request_data)
        return Response({"message": "success", "error": False})
