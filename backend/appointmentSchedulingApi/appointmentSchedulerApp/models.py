from django.db import models
from authapp.models import Patient, Doctor


class Appointment(models.Model):
    """Appointment model"""
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('attended', 'Attended'),
        ('canceled', 'Canceled'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.appointment_date} at {self.appointment_time}"