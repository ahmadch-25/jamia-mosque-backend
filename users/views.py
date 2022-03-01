from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserInfo
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from .serializers import UserSerializer, ContributionSerializer, DonationItems, CampaignSerializer
from campaign.models import CampaignContribution
from fcm_django.models import FCMDevice


class UserRegister(APIView):

    def post(self, request):
        user_data = request.data

        if len(User.objects.filter(username=user_data["email"])) > 0:
            return Response({"message": "User Already Exist With this email!", "error": True},
                            status=status.HTTP_409_CONFLICT)

        user = User(
            username=user_data["email"], email=user_data["email"], first_name=user_data["first_name"],
            last_name=user_data["last_name"], password=user_data["password"]
        )
        user.set_password(user_data["password"])
        user.save()
        app_user = UserInfo(user=user, phone_number=user_data["phone_number"], device_token=user_data["device_token"])
        try:
            fcm_device = FCMDevice(user=user, name=user.first_name, active=True, device_id=user_data["phone_number"],
                                   registration_id=user_data["device_token"], type='android')
        except Exception as e:
            print(e)

        fcm_device.save()
        app_user.save()
        user = UserSerializer(user)
        return Response({"message": "success", "error": False, "user": user.data}, status=status.HTTP_200_OK)


class UserLogin(APIView):

    def post(self, request):
        user_data = request.data

        if len(User.objects.filter(username=user_data["email"])) == 0:
            return Response({"message": "User Not Found !", "error": True}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=user_data["email"])
        if check_password(user_data["password"], user.password):
            fcm_device = FCMDevice.objects.filter(user=user).first()
            fcm_device.registration_id = user_data["device_token"]
            fcm_device.save()
            user = UserSerializer(user)
            return Response({"message": "success", "error": False, "user": user.data}, status=status.HTTP_200_OK)

        return Response({"message": "Password Not Correct !", "error": True}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    """
    An endpoint for changing password.
    """

    def post(self, request, *args, **kwargs):
        request_data = request.data
        user = User.objects.get(email=request_data['email'])
        # Check old password
        if not user.check_password(request_data["old_password"]):
            return Response({"message": "Wrong old password."}, status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        user.set_password(request_data["new_password"])
        user.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': [],
        }

        return Response(response)


class UserUpdate(APIView):

    def post(self, request):
        user_data = request.data

        user = User.objects.filter(email=user_data["email"]).first()

        user.email = user_data["updated_email"]
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.userinfo.phone_number = user_data["phone_number"]
        user.save()
        user = UserSerializer(user)
        return Response({"message": "success", "error": False, "user": user.data}, status=status.HTTP_200_OK)


class UserContributions(APIView):

    def post(self, request):
        user_data = request.data
        donations = CampaignContribution.objects.filter(user__email=user_data['email'])
        contributions_data = ContributionSerializer(donations, many=True)
        return Response({"message": "success", "error": False, "contributions": contributions_data.data},
                        status=status.HTTP_200_OK)
