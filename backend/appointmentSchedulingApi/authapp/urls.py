from django.urls import path

from . import views


urlpatterns = [
    # Auth
    path('doctor/signup/', views.DoctorRegistrationView.as_view(), name='doctor-registration'),
    path('patient/signup/', views.PatientRegistrationView.as_view(), name='patient-registration'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('token-verify/', views.TokenVerifyView.as_view(), name='token-verify'),
]
