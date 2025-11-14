#BloodBank.urls.py
from django.urls import path
from .views import (
    BloodRequestListView,
    BloodRequestUpdateView,
    AlertListCreateView,
    AlertDeleteView,
    BloodBankStatsView,
)

urlpatterns = [
    path('requests/', BloodRequestListView.as_view(), name='blood-requests'),
    path('requests/<int:pk>/', BloodRequestUpdateView.as_view(), name='process-request'),
    path('alerts/', AlertListCreateView.as_view(), name='alerts'),
    path('alerts/<str:blood_group>/', AlertDeleteView.as_view(), name='close-alert'),
    path('stats/', BloodBankStatsView.as_view(), name='bloodbank-stats'),
]