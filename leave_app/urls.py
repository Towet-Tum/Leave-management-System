from django.urls import path
from .views import (
    LeaveApplicationListCreateAPIView,
    LeaveApplicationRetrieveUpdateDestroyAPIView,
    LeaveTypeListCreateAPIView,
    LeaveTypeRetrieveUpdateDestroyAPIView,
    MonthlyLeaveCreditListCreateAPIView,
    MonthlyLeaveCreditRetrieveUpdateDestroyAPIView,
    ApprovalLogListCreateAPIView,
    ApprovalLogRetrieveUpdateDestroyAPIView,
    YearlyLeaveConversionListCreateAPIView,
    YearlyLeaveConversionRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('', LeaveApplicationListCreateAPIView.as_view(), name='leave_applications_list_create'),
    path('<uuid:pk>/', LeaveApplicationRetrieveUpdateDestroyAPIView.as_view(), name='leave_applications_rud'),
    path('leave_types/', LeaveTypeListCreateAPIView.as_view(), name='leave_types_list_create'),
    path('leave_types/<uuid:pk>/', LeaveTypeRetrieveUpdateDestroyAPIView.as_view(), name='leave_types_rud'),
    path('monthly_credits/', MonthlyLeaveCreditListCreateAPIView.as_view(), name='monthly_credits_list_create'),
    path('monthly_credits/<uuid:pk>/', MonthlyLeaveCreditRetrieveUpdateDestroyAPIView.as_view(), name='monthly_credits_rud'),
    path('approval_logs/', ApprovalLogListCreateAPIView.as_view(), name='approval_logs_list_create'),
    path('approval_logs/<uuid:pk>/', ApprovalLogRetrieveUpdateDestroyAPIView.as_view(), name='approval_logs_rud'),
    path('yearly_conversions/', YearlyLeaveConversionListCreateAPIView.as_view(), name='yearly_conversions_list_create'),
    path('yearly_conversions/<uuid:pk>/', YearlyLeaveConversionRetrieveUpdateDestroyAPIView.as_view(), name='yearly_conversions_rud'),
]