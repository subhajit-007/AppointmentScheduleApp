from rest_framework import serializers

from .models import Appointment
from authapp.serializers import PatientSerializer, DoctorSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'notes']


# class AppointmentCreateUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = ['doctor', 'appointment_date', 'appointment_time', 'notes']


class AppointmentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status']

    def validate(self, data):
        patient = data.get('patient')
        doctor = data.get('doctor')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')

        # Check if the patient already has a pending appointment with the same doctor
        if self.instance is None or (self.instance and self.instance.status != 'scheduled'):
            if Appointment.objects.filter(
                patient=patient,
                doctor=doctor,
                status='scheduled'
            ).exists():
                raise serializers.ValidationError("You already have a pending appointment with this doctor.")

        # Check if the patient has another appointment at the same time
        if self.instance is None or (self.instance and self.instance.status != 'scheduled'):
            if Appointment.objects.filter(
                patient=patient,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status='scheduled'
            ).exists():
                raise serializers.ValidationError("You already have an appointment at this time.")

        # Check if the doctor has another appointment at the same time
        if self.instance is None or (self.instance and self.instance.status != 'scheduled'):
            if Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status='scheduled'
            ).exists():
                raise serializers.ValidationError("The doctor is already booked at this time.")

        return data