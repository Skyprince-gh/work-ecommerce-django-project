""" from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from .models import User, PhoneOTP
from django.shortcuts import get_object_or_404
import random
from .serializers import CreateUserSerializer, LoginSerializer
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login


class ApiOverview(APIView):
    def get(self, request, *args, **kwargs):
        api_urls = {
            'Validate phone': '/validate_phone',
            'Validate OTP': '/validate_otp',
            'Register': '/register',
            'Log in': '/login',
            'Log out': '/logout/'
        }
        return Response(api_urls)

class ValidatePhone(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detial': 'phone number already exists'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'status': False,
                                'detail': 'OTP limit exeeded contact customer care'
                            })
                        old.count = count + 1
                        old.save()
                        print(f"count increased to {count}")
                        print(key)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully'
                        })
                    else:
                        PhoneOTP.objects.create(
                            phone = phone,
                            otp = key,
                        )
                        return Response({
                            'status': True,
                            'detial': 'OTP sent successfully'
                        })
                else:
                    return Response({
                        'status': False,
                        'detial': 'Eror sending opt'
                    })
        else:
            return Response({
                'status' : False,
                'detail' : 'Phone number is not provided'
            })




def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        return key
    else:
        return False



class ValidateOTP(APIView):
    # If user is validated, the person will be redirected to set password

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'Please proceed to register'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect'
                    })


class Register(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)

        if  phone and password:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                validated = old.validated
                if validated:
                    temp_data = {
                        'phone': phone,
                        'password': password
                    }
                    serializer = CreateUserSerializer(data = temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    old.delete
                    return Response({
                        'status': True,
                        'detail': 'Account successfully created'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Phone number is not verified'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Please verify phone first'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Phone and password not sent'
            })


class Login(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )


    def post(self, request, format=None):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
 """