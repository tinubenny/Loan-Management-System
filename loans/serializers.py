from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
from django.conf import settings
import subprocess
from .models import Loan, LoanRepayment

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
            print(f" Error sending OTP email: {e}")

        return user
    
class LoanSerializer(serializers.ModelSerializer):
    total_payable = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    monthly_installment = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    interest_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining_balance = serializers.SerializerMethodField() 
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'status', 'total_payable', 'monthly_installment', 'interest_amount', 'remaining_balance']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        loan = super().create(validated_data)
        loan.calculate_loan_details()  # ✅ Automatically calculates interest & installment
        return loan

    def get_remaining_balance(self, obj):
        return obj.calculate_remaining_balance()


# Loan Repayment Serializer
class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = '__all__'
        read_only_fields = ['user', 'payment_date']

    def create(self, validated_data):
        """Ensure payments are valid and update loan status when fully repaid"""
        validated_data['user'] = self.context['request'].user  # Assign user automatically
        repayment = LoanRepayment.objects.create(**validated_data)

        # Check if loan is fully paid
        loan = repayment.loan
        total_paid = sum(p.amount_paid for p in LoanRepayment.objects.filter(loan=loan))
        
        if total_paid >= loan.total_payable:
            loan.status = "paid"
            loan.save()
        
        return repayment
    
# Loan Foreclosure Serializer
class LoanForeclosureSerializer(serializers.ModelSerializer):
    adjusted_total_payable = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'user', 'amount', 'interest_rate', 'term', 'status', 'total_payable', 'adjusted_total_payable']
        read_only_fields = ['user', 'total_payable', 'adjusted_total_payable']

    def update(self, instance, validated_data):
        """Foreclose loan with adjusted interest"""
        adjusted_amount = instance.foreclose_loan()  # Auto-calculate adjusted payment
        instance.save()
        return instance
    
class AdminLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'total_payable', 'monthly_installment', 'interest_amount']

    def update(self, instance, validated_data):
        """Allow admin to approve/reject loans"""
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance