import json

from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .serializers import AppointmentSerializer, AppointmentCreateUpdateSerializer
from .models import Appointment

from authapp.models import Patient, Doctor
from authapp.serializers import PatientSerializer, DoctorSerializer


# Patient views
# class AppointmentListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = AppointmentCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Appointment.objects.filter(patient__user=self.request.user)
#
#     def perform_create(self, serializer):
#         patient = Patient.objects.get(user=self.request.user)
#         doctor = serializer.validated_data['doctor']
#         appointment_date = serializer.validated_data['appointment_date']
#         appointment_time = serializer.validated_data['appointment_time']
#
#         # Check if the patient already has a pending appointment with the same doctor
#         if Appointment.objects.filter(
#             patient=patient,
#             doctor=doctor,
#             status='scheduled'
#         ).exists():
#             raise ValidationError("You already have a pending appointment with this doctor.")
#
#         # Check if the patient has another appointment at the same time
#         if Appointment.objects.filter(
#             patient=patient,
#             appointment_date=appointment_date,
#             appointment_time=appointment_time,
#             status='scheduled'
#         ).exists():
#             raise ValidationError("You already have an appointment at this time.")
#
#         # Check if the doctor has another appointment at the same time
#         if Appointment.objects.filter(
#             doctor=doctor,
#             appointment_date=appointment_date,
#             appointment_time=appointment_time,
#             status='scheduled'
#         ).exists():
#             raise ValidationError("The doctor is already booked at this time.")
#
#         serializer.save(patient=patient)


class AppointmentListCreateAPIView(APIView):
    serializer_class = AppointmentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(patient__user=self.request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        patient = Patient.objects.get(user=self.request.user)

        serializer = AppointmentCreateUpdateSerializer(data=json.loads(request.body), context={'user': request.user})

        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(patient__user=self.request.user)


# class AppointmentCancelUpdateAPIView(generics.UpdateAPIView):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         # Allow only the patient who owns the appointment to access it
#         return Appointment.objects.filter(patient__user=self.request.user, status='scheduled')
#
#     def perform_update(self, serializer):
#         appointment = self.get_object()
#         current_time = timezone.now()
#
#         valid_appointment_check = appointment.appointment_date < current_time.date() or (appointment.appointment_date == current_time.date() and appointment.appointment_time <= current_time.time())
#         # Ensure the appointment is not in the past
#         if valid_appointment_check:
#             raise ValidationError(
#                 "You cannot update or cancel an appointment that is in the past or at the current time.")
#
#         # Update or cancel the appointment
#         status = self.request.data.get('status', None)
#         if status:
#             if status not in ['attended', 'canceled']:
#                 raise ValidationError("Invalid status. Status must be either 'attended' or 'canceled'.")
#             serializer.save(status=status)
#         else:
#             # Update other fields if status is not provided
#             serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentCancelUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, patient__user=request.user, status='scheduled')
        except Appointment.DoesNotExist:
            return Response({"detail": "Appointment Not found."}, status=status.HTTP_404_NOT_FOUND)

        current_time = timezone.now()

        appointment_update_is_not_valid = appointment.appointment_date < current_time.date() or (appointment.appointment_date == current_time.date() and appointment.appointment_time <= current_time.time())
        # Ensure the appointment is not in the past
        if appointment_update_is_not_valid:
            raise ValidationError("You cannot update or cancel an appointment that is in the past or at the current time.")

        serializer = AppointmentCreateUpdateSerializer(appointment, data=json.loads(request.body), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Doctor views
class DoctorAppointmentListAPIView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(doctor__user=self.request.user)


# class AppointmentStatusUpdateAPIView(generics.UpdateAPIView):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Appointment.objects.filter(doctor__user=self.request.user)
#
#     def perform_update(self, serializer):
#         status = self.request.data.get('status')
#         if status not in ['attended', 'canceled']:
#             raise ValidationError("Invalid status. Status must be either 'attended' or 'canceled'.")
#
#         serializer.save(status=status)
#

class AppointmentStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, doctor__user=request.user)
        except Appointment.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        status_value = json.loads(request.body).get('status')
        if status_value not in ['attended', 'canceled']:
            raise ValidationError("Invalid status. Status must be either 'attended' or 'canceled'.")

        serializer = AppointmentCreateUpdateSerializer(appointment, data=json.loads(request.body), partial=True)
        if serializer.is_valid():
            serializer.save(status=status_value)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientHistoryAPIView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(doctor__user=self.request.user, patient_id=self.kwargs['patient_id'])


# Search for doctors by specialty and availability
class DoctorSearchAPIView(APIView):
    def get(self, request):
        specialty = request.query_params.get('specialty', None)
        if specialty:
            doctors = Doctor.objects.filter(specialty__icontains=specialty)
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

