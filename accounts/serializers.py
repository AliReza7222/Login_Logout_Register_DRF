from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import MyUser


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'confirm_password']


    def validate_password(self, value):
        if len(value) <= 6:
            raise serializers.ValidationError("Password must be 6 characters longer !")
        return value

    def validate(self, data):
        password, confirm = data['password'], data['confirm_password']
        if password != confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        del validated_data['confirm_password']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
