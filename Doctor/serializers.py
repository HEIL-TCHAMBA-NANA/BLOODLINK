# serializers.py
"""
from rest_framework import serializers
from .models import BloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = ['id', 'blood_group', 'quantity', 'urgency', 'status', 'hospital']
"""
"""
from rest_framework import serializers
from .models import BloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
    doctor_email = serializers.EmailField(source='doctor.email', read_only=True)
    doctor_id = serializers.IntegerField(source='doctor.id', read_only=True)
    
    class Meta:
        model = BloodRequest
        fields = '__all__'
        # Ou spécifiez : fields = ['id', 'blood_group', 'quantity', 'urgency', 'hospital', 'status', 'created_at', 'doctor', 'doctor_email', 'doctor_id']
"""

from rest_framework import serializers
from .models import BloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
    doctor_email = serializers.EmailField(source='doctor.email', read_only=True)
    
    class Meta:
        model = BloodRequest
        fields = ['id', 'blood_group', 'quantity', 'urgency', 'hospital', 'status', 'created_at', 'doctor', 'doctor_email']
        read_only_fields = ['id', 'created_at', 'status', 'doctor', 'doctor_email']  # ✅ Ajoutez 'doctor' ici