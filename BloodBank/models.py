#models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BloodRequest(models.Model):
    URGENCY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    hospital = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    quantity = models.CharField(max_length=20)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    status = models.CharField(max_length=20, default='pending')  # pending, processed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} - {self.blood_group} ({self.status})"


class Alert(models.Model):
    blood_bank = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    blood_group = models.CharField(max_length=5)
    radius = models.FloatField()
    duration = models.IntegerField(help_text="Duration in hours")
    donor_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert {self.blood_group} - Active: {self.is_active}"