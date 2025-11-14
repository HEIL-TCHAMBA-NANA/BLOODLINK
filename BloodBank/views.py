from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from Doctor.models import BloodRequest  # ✅ get doctor requests
from Donor.models import DonorAlertResponse  # ✅ to count accepted donors
from .serializers import BloodRequestSerializer, AlertSerializer
from users.models import DonorProfile
from rest_framework.views import APIView


class BloodRequestListView(generics.ListAPIView):
    """GET /api/bloodbank/requests/ — list all active requests"""
    queryset = BloodRequest.objects.filter(status='pending')
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated]


class BloodRequestUpdateView(generics.UpdateAPIView):
    """PATCH /api/bloodbank/requests/<id>/ — mark request as processed"""
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get('status', instance.status)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AlertListCreateView(generics.ListCreateAPIView):
    """
    GET /api/bloodbank/alerts/ — List active alerts
    POST /api/bloodbank/alerts/ — Create new alert
    """
    queryset = Alert.objects.filter(is_active=True)
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Return just the alerts list for simplicity"""
        alerts = self.get_queryset()
        serializer = self.get_serializer(alerts, many=True)
        
        # ✅ Retourner directement la liste au lieu d'un objet
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(
            donor_count=0,
            blood_bank=self.request.user  # associe automatiquement à l'utilisateur connecté
        )



class BloodBankStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Compter les donneurs disponibles
        available_donors = DonorProfile.objects.filter(is_available=True).count()
        
        # Compter par groupe sanguin
        blood_groups_stats = {}
        for blood_group in ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']:
            count = DonorProfile.objects.filter(
                blood_group=blood_group, 
                is_available=True
            ).count()
            blood_groups_stats[blood_group] = count
        
        return Response({
            'available_donors': available_donors,
            'blood_groups': blood_groups_stats
        }, status=status.HTTP_200_OK)


class AlertDeleteView(generics.DestroyAPIView):
    """DELETE /api/bloodbank/alerts/<blood_group>/ — deactivate an alert"""
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        blood_group = self.kwargs['blood_group']
        return Alert.objects.filter(blood_group=blood_group, is_active=True).first()

    def destroy(self, request, *args, **kwargs):
        alert = self.get_object()
        if not alert:
            return Response({"detail": "Alert not found."}, status=status.HTTP_404_NOT_FOUND)
        alert.is_active = False
        alert.save()
        return Response(status=status.HTTP_204_NO_CONTENT)