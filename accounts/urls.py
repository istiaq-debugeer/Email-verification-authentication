from django.urls import path

from .utils import verify
from . import views
from knox.views import LogoutView,LogoutAllView

urlpatterns = [
    path('login/',views.LoginAPIView.as_view(),name='login'),

    path('index/',views.home.as_view(), name='index'),
    path('edit/',views.edit_view.as_view(),name='edit_view'),
    path('profile/', views.profile.as_view(), name='profile'),
    path('register/', views.register_view.as_view(), name='register'),
    path('user/',views.user.as_view(),name='user'),
    path('edit/<int:pk>/', views.edit.as_view(), name="edit"),
    path('verify/<token>', verify, name="verify"),
    # path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
]