from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UserProfile, CustomUser
from django.contrib.auth.hashers import make_password


class UserProfilesirealizer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'fullname', 'phone', 'address', 'password', 'is_verified', 'token')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        # token = validated_data.pop('token', None)
        # instance = super().create(validated_data)
        # instance.token = token
        # instance.save()

        return UserProfile.objects.create(**validated_data)




    def update(self, instance, validated_data):
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)

        instance.save()
        return instance


class CustomUserserializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'fullname', 'email', 'password', 'phone', 'address', 'gender')

    def create(self, validated_data):

        custom_user = CustomUser.objects.create_user(**validated_data)

        return custom_user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'},trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')
        print(f'Email: {email}, Password: {password}')
        if not email or not password:
            raise serializers.ValidationError("plese filled both email and password")

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("email does not exist")

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        print(f'User: {user}')
        if not user:
            raise serializers.ValidationError("wrong Credential")

        attrs['user'] = user
        return attrs

c
