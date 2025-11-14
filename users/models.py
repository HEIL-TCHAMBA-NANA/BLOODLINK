from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='donor', **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('donor', 'Donor'),
        ('doctor', 'Doctor'),
        ('bloodbank', 'Blood Bank'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Fix for reverse accessor clash
    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',  # avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users_permissions',  # avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.email} ({self.role})"


# Profile models
class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3)
    date_of_birth = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)


    def __str__(self):
        return self.user.email

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    professional_id = models.CharField(max_length=50)
    hospital = models.CharField(max_length=100)

class BloodBankProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_profile')
    bank_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
