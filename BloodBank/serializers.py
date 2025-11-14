#serializers.py
from rest_framework import serializers
from .models import BloodRequest, Alert

class BloodRequestSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.username', read_only=True)

    class Meta:
        model = BloodRequest
        fields = ['id', 'urgency', 'doctor', 'hospital', 'blood_group', 'quantity', 'status']


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['blood_group', 'radius', 'duration', 'donor_count', 'is_active']