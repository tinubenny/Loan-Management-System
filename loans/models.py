from django.contrib.auth.models import AbstractUser
from django.db import models
import math
from datetime import datetime


# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User')
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.username
    
class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)  # Annual interest %
    term = models.IntegerField()  # Tenure in months
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Auto-Calculated Fields
    total_payable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calculate_remaining_balance(self):
        """Calculate remaining balance by subtracting total repayments from total payable."""
        total_paid = sum(payment.amount_paid for payment in self.loanrepayment_set.all())
        return self.total_payable - total_paid

    def save(self, *args, **kwargs):
        """Auto-calculate total_payable & monthly installment if not set"""
        if self.total_payable is None or self.monthly_installment is None:
            interest_amount = (self.amount * (self.interest_rate / 100) * (self.term / 12))
            self.total_payable = self.amount + interest_amount
            self.monthly_installment = self.total_payable / self.term
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.id} - {self.user.username}"

    def calculate_loan_details(self):
        """Calculate total interest and monthly installment"""
        r = float(self.interest_rate) / 100 / 12  # Monthly interest rate
        n = int(self.term)  # Number of months
        p = float(self.amount)  # Principal

        # Compound Interest Formula: A = P * (1 + r)^n
        total_amount = p * math.pow((1 + r), n)
        self.total_payable = round(total_amount, 2)
        self.interest_amount = round(self.total_payable - p, 2)
        self.monthly_installment = round(self.total_payable / n, 2)
        self.save()

    def foreclose_loan(self):
        """Calculate adjusted total payable and update status to paid"""
        current_date = datetime.now()
        months_passed = (current_date.year - self.created_at.year) * 12 + (current_date.month - self.created_at.month)

        if months_passed > 0:
            interest_due = (self.amount * (self.interest_rate / 100) * (months_passed / 12))
        else:
            interest_due = 0  # No extra interest if foreclosed immediately

        adjusted_total_payable = self.amount + interest_due

        self.total_payable = adjusted_total_payable
        self.status = "paid"  #  Update loan status to paid
        self.save()
        return adjusted_total_payable

    def __str__(self):
        return f"Loan {self.id} - {self.user.username}"

# Loan Repayment Model
class LoanRepayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} paid {self.amount_paid} on {self.payment_date}"