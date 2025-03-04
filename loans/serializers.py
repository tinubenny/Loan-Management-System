from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
from django.conf import settings
import subprocess
from .models import Loan


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True , required=False)
    role = serializers.ChoiceField(choices=[('admin', 'Admin'), ('user', 'User')], required=False)
                                   
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'otp']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        otp = str(random.randint(100000, 999999))
        role = validated_data.get('role', 'user')
        is_admin = role == "admin"

        # ✅ Generate a default username if not provided
        username = validated_data.get('username', validated_data['email'].split('@')[0])

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            role=role,
            is_staff=is_admin,  # ✅ Admins get staff privileges
            is_superuser=is_admin,  # ✅ Admins get superuser privileges
        )

        user.is_verified = False
        user.otp = otp
        user.save()

        # ✅ Try sending email, but handle errors safely
        try:
            subprocess.run(["node", "send_email.js", user.email, otp], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error sending OTP email: {e}")

        return user
    
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'status']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)