from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.id}. {self.username}"


class Doctor(models.Model):
    """User doctor"""
    doctor_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    specialty = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_account")

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialty}"


class Patient(models.Model):
    """User patient"""
    patient_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    phone_number = models.CharField(max_length=10, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_account")

    def __str__(self):
        return f"{self.id}. {self.user.username}"