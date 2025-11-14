from django.urls import path
from .views import (
    DonorAlertsView, 
    DonorAvailabilityUpdate, 
    RespondToAlert,
    DonorMeView,
    DonorMeAvailabilityUpdate  # ✅ Ajoutez cet import
)

urlpatterns = [
    path('me/', DonorMeView.as_view(), name='donor-me'),
    path('me/availability/', DonorMeAvailabilityUpdate.as_view(), name='donor-me-availability'),
    path('alerts/', DonorAlertsView.as_view(), name='donor-alerts'),
    path('availability/<int:pk>/', DonorAvailabilityUpdate.as_view(), name='update-availability'),
    path('alerts/<int:alert_id>/<str:action>/', RespondToAlert.as_view(), name='respond-alert'),
]