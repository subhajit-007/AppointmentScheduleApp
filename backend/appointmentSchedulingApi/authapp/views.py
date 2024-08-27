import json

from .models import User, Patient, Doctor
from .serializers import UserSerializer, DoctorSerializer, PatientSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class DoctorRegistrationView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientRegistrationView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        print("data ==> ", data)
        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(ObtainAuthToken):
    """"Login view for any user"""
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }

            # Doctor login
            if user.role == 'Doctor':
                doctor = user.doctor_account  # As the related name is "doctor_account"
                if doctor is not None:
                    # Add doctor data to the response data
                    doctor_data = DoctorSerializer(doctor).data
                    response_data['data'] = doctor_data
            # Patient login
            elif user.role == 'patient':
                patient = user.patient_account
                if patient is not None:
                    # Add patient data to the response data
                    patient_data = PatientSerializer(patient).data
                    response_data['data'] = patient_data

            return Response(response_data)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()
        return Response({'detail': 'Successfully logged out.'})


class TokenVerifyView(APIView):
    """Class to verify user token for auth"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "Token is valid"}, status=status.HTTP_200_OK)