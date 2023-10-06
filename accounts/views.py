import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from knox import views as knox_views
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from rest_framework import generics, status, request
from django.urls import reverse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from rest_framework.permissions import AllowAny
from .utils import send_mail_verification,Util
from django.contrib import messages
from .models import CustomUser, UserProfile
from .serializers import UserProfilesirealizer, CustomUserserializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

class register_view(generics.CreateAPIView):
    serializer_class = CustomUserserializer
    # serializer_class=UserProfilesirealizer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = CustomUserserializer(data=request.data)
        if serializer.is_valid():

            custom_user = serializer.save()

            # user_data=serializer.data
            token = str(uuid.uuid4())
            send_mail_verification(custom_user, token)
            # user=CustomUser.objects.get(email=user_data['email'])
            # token=RefreshToken.for_user(user).access_token
            #
            # current_site=get_current_site(request).domain
            # relativeLink= reverse('email-verify')
            # absurl='http://'+current_site+relativeLink+"?token="+str(token)
            #
            # email_body='HI'+user.fullname+'Use link below to verify your email \n'+absurl
            # data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
            # Util.send_mail(data)

            profile_data = {
                'user': custom_user.id,
                'password':request.data.get('password'),
                'profile_image': request.data.get('profile_image'),
                'phone': request.data.get('phone'),
                'address': request.data.get('address'),
                'fullname': request.data.get('fullname'),
                'token': token,
            }
            profile = UserProfilesirealizer(data=profile_data)

            if profile.is_valid():
                profile.save()

                return redirect('/index')
            else:
                return Response(profile.errors, status=status.HTTP_400_BAD_REQUEST)
            messages.success(request, 'need to verified')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self,request):
        serializer=UserProfilesirealizer.update(data=request.data)


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self,request,format=None):
        serializer=self.serializer_class(data=request.data)
        if  serializer.is_valid(raise_exception=True):
            user=serializer.validated_data['user']
            profile_obj=UserProfile.objects.filter(user=user).first()
            if profile_obj.is_verified:
                login(request,user)
                response=super().post(request,format=None)
            else:
                return Response({'errors': serializer.errors})
        else:
            return Response({'errors':serializer.errors})

        return  Response(response.data,status=status.HTTP_200_OK)


# class VerifyEmail(generics.GenericAPIView):
#
#     def get(self, request):
#         token=request.GET.get('token')
#         try:
#             payload=jwt.decode(token,settings.SECRET_KEY)
#             user=UserProfile.objects.get(id=payload['user_id'])
#
#             if not user.is_verified:
#                 user.is_verified=True
#                 user.save()
#
#             return Response({'eamil':'successfully activated'},status=status.HTTP_201_CREATED)
#         except jwt.ExpiredSignatureError:
#             messages.error(request, 'Activation Expired')
#             return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.DecodeError:
#             messages.error(request, 'Invalid token')
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class user(APIView):
    def get(self, request):
        queryset = UserProfile.objects.all()
        serializer_class = UserProfilesirealizer(queryset, many=True)

        jsondata = JSONRenderer().render(serializer_class.data)

        return HttpResponse(jsondata)


class edit(generics.UpdateAPIView):
    serializer_class = UserProfilesirealizer
    queryset = UserProfile.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)




class home(View):
    def get(self, request):
        return render(request, 'home.html')


class edit_view(View):
    def ger(self, request):
        return render(request, 'edit.html')


class profile(View):
    def get(self, request):
        profile = CustomUser.objects.first()
        context = {
            'profile': profile
        }
        return render(request, 'profile.html', context=context)
