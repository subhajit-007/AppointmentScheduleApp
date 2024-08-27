from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.urls')),
    path('api/appointments/', include('appointmentSchedulerApp.urls')),
]
