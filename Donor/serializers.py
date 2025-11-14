#serializers.py

from rest_framework import serializers
from .models import Alert, DonorAlertResponse
from users.models import DonorProfile

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorProfile
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class DonorAlertResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorAlertResponse
        fields = '__all__'