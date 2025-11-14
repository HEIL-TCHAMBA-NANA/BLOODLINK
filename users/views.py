from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from .models import User, DoctorProfile, DonorProfile, BloodBankProfile
from .serializers import (
    DoctorProfileSerializer,
    DonorProfileSerializer,
    BloodBankProfileSerializer,
    LoginSerializer,
    DonorRegisterSerializer,
    DoctorRegisterSerializer,
    BloodBankRegisterSerializer
)

# -----------------------------
# Registration Views
# -----------------------------
class DonorRegisterView(generics.CreateAPIView):
    serializer_class = DonorRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        profile = DonorProfile.objects.get(user=user)
        output_serializer = DonorProfileSerializer(profile)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class DoctorRegisterView(generics.CreateAPIView):
    serializer_class = DoctorRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        profile = DoctorProfile.objects.get(user=user)
        output_serializer = DoctorProfileSerializer(profile)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class BloodBankRegisterView(generics.CreateAPIView):
    serializer_class = BloodBankRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        profile = BloodBankProfile.objects.get(user=user)
        output_serializer = BloodBankProfileSerializer(profile)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------
# Profile Views
# -----------------------------
class DoctorProfileView(generics.RetrieveUpdateAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class DonorProfileView(generics.RetrieveUpdateAPIView):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class BloodBankProfileView(generics.RetrieveUpdateAPIView):
    queryset = BloodBankProfile.objects.all()
    serializer_class = BloodBankProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# Login View using JWT
# -----------------------------
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "email": user.email,
            "role": user.role,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
