from django.urls import path

from . import views


# Appointment scheduling urls
urlpatterns = [
    # Patient APIs
    path('', views.AppointmentListCreateAPIView.as_view(), name='appointment-list-create'),
    path('<int:pk>/', views.AppointmentDetailAPIView.as_view(), name='appointment-detail'),
    path('<int:pk>/update/', views.AppointmentCancelUpdateAPIView.as_view(), name='update-appointment'),
    path('<int:pk>/cancel/', views.AppointmentCancelUpdateAPIView.as_view(), name='cancel-appointment'),
    path('doctors/search/', views.DoctorSearchAPIView.as_view(), name='doctor-search'),

    # Doctor APIs
    path('doctor/', views.DoctorAppointmentListAPIView.as_view(), name='doctor-appointment-list'),
    path('doctor/<int:pk>/status/', views.AppointmentStatusUpdateAPIView.as_view(), name='appointment-status-update'),
    path('doctor/patients/<int:patient_id>/history/', views.PatientHistoryAPIView.as_view(), name='patient-history'),
]
