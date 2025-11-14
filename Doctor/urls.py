from django.urls import path
from .views import DoctorBloodRequestListCreateView
from users.views import DoctorProfileView

urlpatterns = [
    path('<int:pk>/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('requests/', DoctorBloodRequestListCreateView.as_view(), name='doctor-requests'),
]