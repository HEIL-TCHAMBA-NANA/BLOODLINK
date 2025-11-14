"""
from rest_framework import generics, permissions
from .models import BloodRequest
from .serializers import BloodRequestSerializer
from Donor.models import Alert

class DoctorBloodRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BloodRequest.objects.filter(doctor=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        blood_request = serializer.save(doctor=self.request.user)
        
        # Mapper l'urgence du doctor vers le format Alert
        urgency_mapping = {
            'Normal': 'normal',
            'Urgent': 'urgent',
            'Extremely Urgent': 'extremely_urgent'
        }
        
        alert_urgency = urgency_mapping.get(blood_request.urgency, 'normal')
        
        # Créer une Alert pour les donneurs
        Alert.objects.create(
            hospital=blood_request.hospital,
            blood_group=blood_request.blood_group,
            distance="5 km",
            urgency=alert_urgency,
            is_active=True
        )
        
        print(f"✅ Created Alert for blood group {blood_request.blood_group} at {blood_request.hospital}")
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import BloodRequest
from .serializers import BloodRequestSerializer
from Donor.models import Alert

class DoctorBloodRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BloodRequest.objects.filter(doctor=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")
        print(f"User: {request.user}")
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # ✅ Sauvegarder avec le doctor automatiquement
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # ✅ Ajouter le doctor (l'utilisateur connecté) avant de sauvegarder
        blood_request = serializer.save(doctor=self.request.user)
        
        # Mapper l'urgence
        urgency_mapping = {
            'Normal': 'normal',
            'Urgent': 'urgent',
            'Extremely Urgent': 'extremely_urgent'
        }
        
        alert_urgency = urgency_mapping.get(blood_request.urgency, 'normal')
        
        # Créer une Alert pour les donneurs
        Alert.objects.create(
            hospital=blood_request.hospital,
            blood_group=blood_request.blood_group,
            distance="5 km",
            urgency=alert_urgency,
            is_active=True,
            donor_count=0
        )
        
        print(f"✅ Created BloodRequest and Alert for {blood_request.blood_group}")