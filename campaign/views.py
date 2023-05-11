from django.shortcuts import render, redirect
import json
from datetime import datetime

from firebase_admin import messaging
# from intasend import APIService
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mails import wellcomeEmail
from users.models import UserInfo
from users.serializers import UserSerializer
from .serializer import CampaignSerializer
from .models import DonationItems, CampaignContribution, ZakatNisab

# from intasend.utils import generate_keys
from django.contrib.auth.models import User
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from pyIslam.zakat import Zakat

private_key = """-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwhxnB5aZD6EqF....8laHwYTQdDbAlCGZB992YoHl
    -----END PRIVATE KEY-----"""
token = "a8184850d012267e3d717491a2c99cbb3545efbbdc0bf1275291c492faff41a0"
publishable_key = "ISPubKey_test_13a61255-5b3a-4342-964e-04e49616e8c0"
zakat = Zakat()


class CampaignListView(APIView):

    def get(self, request):
        donations_items = DonationItems.objects.filter(publish=True)
        donations_items = CampaignSerializer(donations_items, many=True)
        print(donations_items.data)
        return Response(donations_items.data, status=status.HTTP_200_OK)


def index(request):
    # send_message parameters include: message, dry_run, app
    FCMDevice.objects.send_message(Message(
        notification=Notification(title="Payment Received",
                                  body="Your payment of {} for Donation is Completed, Thank you".format(
                                      10),
                                  image="https://cdn3.iconfinder.com/data/icons/fintech-43/32/FINTECH_RAW_-_FILLED_FLAT-05-512.png"),
    ))
    return render(request, "index.html")


class GenrateCheckoutLink(APIView):
    def post(self, request):
        request_data = request.data


class GenratePaymentUrl(APIView):

    def post(self, request):
        request_data = request.data
        service = None#APIService(token=token, publishable_key=publishable_key, private_key=private_key, test=True)
        if request_data["is_login"]:
            user = User.objects.filter(email=request_data["email"]).first()
            response = service.collect.checkout(
                phone_number=request_data["phone_number"],
                email=request_data["email"],
                amount=request_data["amount"],
                currency="KES",
                comment="Fees",
                first_name=request_data["first_name"],
                last_name=request_data["last_name"],
                api_ref=str(request_data["campaign_id"])+"_"+str(user.id)
            )
        else:
            if User.objects.filter(email=request_data["email"]).exists():
                user = User.objects.filter(email=request_data["email"]).first()
                response = service.collect.checkout(
                    phone_number=request_data["phone_number"],
                    email=request_data["email"],
                    amount=request_data["amount"],
                    currency="KES",
                    comment="Fees",
                    first_name=user.first_name,
                    last_name=user.last_name,
                    api_ref=str(request_data["campaign_id"])+"-"+str(user.id)
                )
                return Response({
                                "message": "success",
                                 "error": False,
                                 "url": response["url"]},
                                status=status.HTTP_200_OK)
            response = service.collect.checkout(
                phone_number=request_data["phone_number"],
                email=request_data["email"],
                amount=request_data["amount"],
                currency="KES",
                comment="Fees",
                first_name=request_data["first_name"],
                last_name=request_data["last_name"],
                api_ref=str(request_data["campaign_id"])
            )
            password = User.objects.make_random_password()
            user = User(
                username=request_data["email"], email=request_data["email"], first_name=request_data["first_name"],
                last_name=request_data["last_name"], password=password
            )
            user.set_password(password)
            user.save()
            wellcomeEmail(user.email,
                          password
                            )
            app_user = UserInfo(user=user, phone_number=request_data["phone_number"],
                                device_token=request_data["device_token"])
            try:
                fcm_device = FCMDevice(user=user, name=user.first_name, active=True,
                                       device_id=request_data["email"],
                                       registration_id=request_data["device_token"], type='android')
            except Exception as e:
                print(e)

            fcm_device.save()
            app_user.save()
            user = UserSerializer(user)
        return Response({"message": "success", "error": False, "url": response["url"], "user": user.data}, status=status.HTTP_200_OK)


class CalculateZakat(APIView):

    def get(self, request):
        currency = request.query_params.get('cur')
        amount = request.query_params.get('amount')
        zakat_nisab = ZakatNisab.objects.all().first()
        if currency == "USD":
            calculated_amount = zakat.calculate_zakat(amount=float(amount), nisab=zakat_nisab.nisab_in_usd)
        else:
            calculated_amount = zakat.calculate_zakat(amount=float(amount), nisab=zakat_nisab.nisab_in_kes)
        return Response({"message": "success", "error": False, 'calculated_amount': calculated_amount},
                        status=status.HTTP_200_OK)


class ListenWebHook(APIView):

    def post(self, request):
        request_data = request.data
        if request_data["state"] == "COMPLETE":
            api_info = request_data["api_ref"].split("-")
            print(api_info)
            user = User.objects.get(pk=api_info[1])
            campaign = DonationItems.objects.first()
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
