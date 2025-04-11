
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('employee_service.urls')),
    path('api/leave/', include('leave_app.urls')),
]
