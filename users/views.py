from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserInfo
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from .serializers import UserSerializer, ContributionSerializer, DonationItems, CampaignSerializer
from campaign.models import CampaignContribution
from fcm_django.models import FCMDevice
from mails import accountVarificationEmail,resetPasswordEmail
from .tokens import account_activation_token


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
        user.is_active = False
        user.save()
        accountVarificationEmail(user.first_name+" "+user.last_name,
                                 user.email,
                                 urlsafe_base64_encode(force_bytes(user.pk)),
                                 account_activation_token.make_token(user)
                                 )
        app_user = UserInfo(user=user, phone_number=user_data["phone_number"], device_token=user_data["device_token"])
        try:
            fcm_device = FCMDevice(user=user, name=user.first_name, active=True, device_id=user_data["phone_number"],
                                   registration_id=user_data["device_token"], type='android')
        except Exception as e:
            print(e)

        fcm_device.save()
        app_user.save()
        user = UserSerializer(user)
        return Response({"message": "success, Varification Email sent!", "error": False, "user": user.data}, status=status.HTTP_200_OK)


class UserLogin(APIView):

    def post(self, request):
        user_data = request.data

        if len(User.objects.filter(username=user_data["email"])) == 0:
            return Response({"message": "User Not Found !", "error": True}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=user_data["email"])
        if user.is_active:
            if check_password(user_data["password"], user.password):
                fcm_device = FCMDevice.objects.filter(user=user).first()
                fcm_device.registration_id = user_data["device_token"]
                fcm_device.save()
                user = UserSerializer(user)
                return Response({"message": "success", "error": False, "user": user.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Password Not Correct !", "error": True},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Account not verified please check verification email", "error": True}, status=status.HTTP_403_FORBIDDEN)



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


class ResetPassword(APIView):

    def post(self, request):
        try:
            user_data = request.data
            user = User.objects.get(email=user_data["email"])

            resetPasswordEmail(
                user.email,
                urlsafe_base64_encode(force_bytes(user.pk)),
                account_activation_token.make_token(user)
            )
            return Response({"message": "reset password email sent", "error": False},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found", "error": True},
                            status=status.HTTP_200_OK)

def activate(request, uidb64, token):
    print(uidb64)
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    print(user)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def genrate_new_password(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    print(user)
    if user is not None and account_activation_token.check_token(user, token):
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        res="""
        Your password reset is successfull . you can login with the following password {}
        """.format(password)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
