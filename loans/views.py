from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoanSerializer
from .models import Loan
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser 





# Create your views here.
User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        # ✅ Use filter() instead of get() to handle multiple users with the same email
        users = User.objects.filter(email=email, otp=otp)

        if users.exists():
            for user in users:
                user.is_verified = True  # ✅ Mark user as verified
                user.otp = None  # ✅ Clear OTP after successful verification
                user.save()
            return Response({"message": "OTP verified successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid OTP or User not found"}, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        
        if not user.is_verified:  # ✅ Prevent unverified users from logging in
            return Response({"error": "Please verify your OTP before logging in."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=user.username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)  # ✅ Generate JWT Token
            return Response({
                "message": "Login successful!",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        
class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LoanListView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Only authenticated users can access

    def get(self, request):
        # ✅ If the user is an admin, show all loans
        if request.user.role == "admin":
            loans = Loan.objects.all()  # ✅ Show all loans
        else:
            loans = Loan.objects.filter(user=request.user)  # ✅ Show only the user's loans

        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)
    
class LoanUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, loan_id):
        try:
            loan = Loan.objects.get(id=loan_id)
            status = request.data.get('status')

            if status not in ['approved', 'rejected']:
                return Response({"error": "Invalid status"}, status=400)

            loan.status = status
            loan.save()
            return Response({"message": f"Loan {status} successfully!"})

        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=404) 
    