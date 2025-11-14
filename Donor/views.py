from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Alert, DonorAlertResponse
from .serializers import AlertSerializer, DonorAlertResponseSerializer, DonorSerializer
from users.models import DonorProfile, DoctorProfile

# Endpoint pour obtenir le profil du donneur connecté
class DonorMeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            donor = DonorProfile.objects.get(user=request.user)
            serializer = DonorSerializer(donor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DonorProfile.DoesNotExist:
            return Response(
                {"error": "Donor profile not found for this user"}, 
                status=status.HTTP_404_NOT_FOUND
            )

# ✅ NOUVEAU: Mettre à jour la disponibilité du donneur connecté
class DonorMeAvailabilityUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            donor = DonorProfile.objects.get(user=request.user)
            donor.is_available = request.data.get('is_available', donor.is_available)
            donor.save()
            return Response({
                "message": "Availability updated successfully",
                "is_available": donor.is_available
            }, status=status.HTTP_200_OK)
        except DonorProfile.DoesNotExist:
            return Response(
                {"error": "Donor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

# ✅ NOUVEAU: Endpoint pour les alertes filtrées par groupe sanguin du donneur
class DonorAlertsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            donor = DonorProfile.objects.get(user=request.user)
            
            print(f"Donor blood group: '{donor.blood_group}'")
            
            # ✅ Exclure les alertes déjà acceptées par ce donneur
            already_accepted_alert_ids = DonorAlertResponse.objects.filter(
                donor=donor,
                accepted=True
            ).values_list('alert_id', flat=True)
            
            # Filtrer les alertes actives par groupe sanguin, en excluant celles déjà acceptées
            alerts = Alert.objects.filter(
                is_active=True,
                blood_group=donor.blood_group
            ).exclude(
                id__in=already_accepted_alert_ids
            ).order_by('-created_at')
            
            print(f"Found {alerts.count()} alerts for blood group {donor.blood_group} (excluding already accepted)")
            
            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DonorProfile.DoesNotExist:
            return Response(
                {"error": "Donor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

# List all alerts
class AlertListView(generics.ListAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctorprofile'):
            return Alert.objects.filter(is_active=True).order_by('-created_at')
        return Alert.objects.filter(is_active=True).order_by('-created_at')

# Doctor can view a specific alert
class DoctorAlertDetailView(generics.RetrieveAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctorprofile'):
            return Alert.objects.filter(is_active=True)
        return Alert.objects.none()

# Donor availability update (ancien endpoint avec ID)
class DonorAvailabilityUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            donor = DonorProfile.objects.get(pk=pk)
            donor.is_available = request.data.get('is_available', donor.is_available)
            donor.save()
            return Response({"message": "Availability updated"}, status=status.HTTP_200_OK)
        except DonorProfile.DoesNotExist:
            return Response({"error": "Donor not found"}, status=status.HTTP_404_NOT_FOUND)

# Donor responds to alert
class RespondToAlert(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, alert_id, action):
        try:
            donor_id = request.data.get("donor_id")
            donor = DonorProfile.objects.get(pk=donor_id)
            alert = Alert.objects.get(pk=alert_id)
            accepted = True if action == "accept" else False

            response_obj, created = DonorAlertResponse.objects.get_or_create(
                donor=donor,
                alert=alert,
                defaults={"accepted": accepted}
            )

            if not created:
                response_obj.accepted = accepted
                response_obj.save()

            if accepted:
                alert.donor_count = DonorAlertResponse.objects.filter(alert=alert, accepted=True).count()
                alert.save(update_fields=["donor_count"])

            return Response({
                "message": f"Alert {'accepted' if accepted else 'rejected'} successfully",
                "donor_count": alert.donor_count
            }, status=status.HTTP_201_CREATED)
        except DonorProfile.DoesNotExist:
            return Response({"error": "Donor not found"}, status=status.HTTP_404_NOT_FOUND)
        except Alert.DoesNotExist:
            return Response({"error": "Alert not found"}, status=status.HTTP_404_NOT_FOUND)