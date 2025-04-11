from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (LogoutView,
                    EmployeeListView,
                    EmployeeDetailView,
                    EmployeeRegistrationView
                    )

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('employee/', EmployeeListView.as_view(), name='employee'),
    path('employee/<str:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    
]
