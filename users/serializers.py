# auth_app/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, DonorProfile, DoctorProfile, BloodBankProfile


# -------------------------------
# LOGIN SERIALIZER
# -------------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        # Django authenticate() expects USERNAME_FIELD — ensure your User model uses email for authentication
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        if user.role.lower() != role.lower():
            raise serializers.ValidationError("Role mismatch")

        data["user"] = user
        return data


# -------------------------------
# REGISTRATION SERIALIZERS
# -------------------------------
class DonorRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    blood_group = serializers.CharField()
    date_of_birth = serializers.DateField(
    format="%d/%m/%Y",
    input_formats=["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d","%Y-%m-%dT%H:%M:%S"]
    )

    class Meta:
        model = User
        fields = ("email", "password", "name", "blood_group", "date_of_birth")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        donor_data = {
            "name": validated_data.pop("name"),
            "blood_group": validated_data.pop("blood_group"),
            "date_of_birth": validated_data.pop("date_of_birth"),
        }

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role="donor",
        )

        DonorProfile.objects.create(user=user, **donor_data)
        return user


class DoctorRegisterSerializer(serializers.ModelSerializer):
    professional_id = serializers.CharField()
    hospital = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "professional_id", "hospital")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        doctor_data = {
            "professional_id": validated_data.pop("professional_id"),
            "hospital": validated_data.pop("hospital"),
        }

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role="doctor",
        )

        DoctorProfile.objects.create(user=user, **doctor_data)
        return user


class BloodBankRegisterSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField()
    location = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "bank_name", "location")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        bank_data = {
            "bank_name": validated_data.pop("bank_name"),
            "location": validated_data.pop("location"),
        }

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role="blood bank",
        )

        BloodBankProfile.objects.create(user=user, **bank_data)
        return user


# -------------------------------
# USER SERIALIZER
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role"]


# -------------------------------
# PROFILE SERIALIZERS
# -------------------------------
class DonorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DonorProfile
        fields = ["user", "name", "blood_group", "date_of_birth"]


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ["user", "professional_id", "hospital"]


class BloodBankProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BloodBankProfile
        fields = ["user", "bank_name", "location"]
