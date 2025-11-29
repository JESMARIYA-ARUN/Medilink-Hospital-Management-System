from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='patient'  # Default role for existing and new users
    )
    # Common fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    # Doctor-only fields
    specialization = models.CharField(max_length=200, blank=True, null=True)
    hospital_contact = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
