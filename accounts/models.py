from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("The email is not given")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.is_active=True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if not extra_fields.get('is_staff'):
            raise ValueError("superuser must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True ")
        return self.create_user(email,password,**extra_fields)




class CustomUser(AbstractBaseUser):
    GENDER_CHOICES=(
        (1,'male'),
        (2,'female'),
        (3,'other')
    )
    email=models.EmailField(max_length=254,unique=True)
    password = models.CharField(max_length=128,null =True)
    first_name=models.CharField(max_length=128,null=True)
    last_name=models.CharField(max_length=128,null=True)
    fullname=models.CharField(max_length=250,null=True)
    # profile=models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    profile_image=models.ImageField(upload_to='user/',null=True,blank=True)
    phone=models.IntegerField(blank=True,null=True)
    address=models.CharField(max_length=250,null=True )
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)
    gender=models.SmallIntegerField(choices=GENDER_CHOICES,null=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=True)
    is_active=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['gender']


    objects=UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self,app_label):
        return True

    def has_perm(self,perm,obj=None):
        return True
# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE ,related_name='profile')
    profile_image=models.ImageField(upload_to='user/',null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    phone=models.IntegerField(blank=True,null=True)
    address=models.CharField(max_length=250)
    fullname=models.CharField(max_length=250)
    password = models.CharField(max_length=128,null =True)
    token=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return self.fullname
