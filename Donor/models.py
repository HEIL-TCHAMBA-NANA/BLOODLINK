#models.py
from django.db import models
from users.models import DonorProfile  # Use the existing donor model

class Alert(models.Model):
    BLOOD_URGENCY = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('extremely_urgent', 'Extremely Urgent'),
    ]
    is_active = models.BooleanField(default=True)
    hospital = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    donor_count = models.IntegerField(default=0)  # ✅ AJOUT
    distance = models.CharField(max_length=50)
    urgency = models.CharField(max_length=20, choices=BLOOD_URGENCY)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert: {self.hospital} ({self.blood_group})"


class DonorAlertResponse(models.Model):
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    accepted = models.BooleanField()
    responded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.user.username} -> {self.alert.hospital} ({'Accepted' if self.accepted else 'Rejected'})"