# auth_app/urls.py
from django.urls import path
from .views import LoginView, DonorRegisterView, DoctorRegisterView, BloodBankRegisterView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/donneur/', DonorRegisterView.as_view(), name='register_donor'),
    path('auth/register/doctor/', DoctorRegisterView.as_view(), name='register_doctor'),
    path('auth/register/blood_bank/', BloodBankRegisterView.as_view(), name='register_bank'),
]
