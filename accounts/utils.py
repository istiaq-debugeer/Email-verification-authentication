from django.contrib.auth import login
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from Ticket_Booking_Syatem import settings
from .models import CustomUser, UserProfile
from .serializers import UserProfilesirealizer
from django.contrib import messages
from django.core.mail import EmailMessage




def send_mail_verification(user, token):
        subject = "Your account needs to be verified"
        messages = f'Hi click your your link to verify your account http://127.0.0.1:8000/verify/{token}'
        email_form = settings.EMAIL_HOST_USER
        recipent_list = [user.email]
        send_mail(subject, messages, email_form, recipent_list)


def verify(request,token):
    try:
        profile_obj=UserProfile.objects.filter(token=token).first()
        if profile_obj:
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,'You account is been verified')
            return Response({'message': 'User verifyed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(profile_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)

class Util:
    @staticmethod
    def send_mail(data):

        email=EmailMessage(subject=data['email_subject'],body=data['email_body'],to=[data['to_email']])
        email.send()
