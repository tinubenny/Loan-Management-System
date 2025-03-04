from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, VerifyOTPView, LoginView, LoanCreateView, LoanListView, LoanUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),  # ✅ OTP Verification
    path('login/', LoginView.as_view(), name='login'),  # ✅ Login
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ JWT Token Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ✅ Refresh JWT Token

    path('loans/apply/', LoanCreateView.as_view(), name='loan-apply'),  # ✅ Apply for a loan
    path('loans/', LoanListView.as_view(), name='loan-list'),  # ✅ View user’s loans
    path('loans/update/<int:loan_id>/', LoanUpdateView.as_view(), name='loan-update'),  # ✅ Approve/reject loans (admin)
]
