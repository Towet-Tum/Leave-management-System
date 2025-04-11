from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import datetime
from .models import LeaveApplication, LeaveType, MonthlyLeaveCredit, ApprovalLog, YearlyLeaveConversion
from .serializers import (
    LeaveApplicationSerializer,
    LeaveTypeSerializer,
    MonthlyLeaveCreditSerializer,
    ApprovalLogSerializer,
    YearlyLeaveConversionSerializer,
)
from .tasks import auto_approve_leave

class LeaveApplicationListCreateAPIView(ListCreateAPIView):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the leave application (credit deduction is handled in serializer.create())
        leave = serializer.save()
        # Schedule auto approval task: run at deadline (24 hours before leave_date)
        leave_date_start = timezone.make_aware(datetime.datetime.combine(leave.leave_date, datetime.time.min))
        deadline = leave_date_start - datetime.timedelta(hours=24)
        delay = (deadline - timezone.now()).total_seconds()
        if delay > 0:
            auto_approve_leave.apply_async(args=[leave.id], countdown=delay)

class LeaveApplicationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]

# Additional views for other models:
class LeaveTypeListCreateAPIView(ListCreateAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]

class LeaveTypeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]

class MonthlyLeaveCreditListCreateAPIView(ListCreateAPIView):
    queryset = MonthlyLeaveCredit.objects.all()
    serializer_class = MonthlyLeaveCreditSerializer
    permission_classes = [IsAuthenticated]

class MonthlyLeaveCreditRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MonthlyLeaveCredit.objects.all()
    serializer_class = MonthlyLeaveCreditSerializer
    permission_classes = [IsAuthenticated]

class ApprovalLogListCreateAPIView(ListCreateAPIView):
    queryset = ApprovalLog.objects.all()
    serializer_class = ApprovalLogSerializer
    permission_classes = [IsAuthenticated]

class ApprovalLogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ApprovalLog.objects.all()
    serializer_class = ApprovalLogSerializer
    permission_classes = [IsAuthenticated]

class YearlyLeaveConversionListCreateAPIView(ListCreateAPIView):
    queryset = YearlyLeaveConversion.objects.all()
    serializer_class = YearlyLeaveConversionSerializer
    permission_classes = [IsAuthenticated]

class YearlyLeaveConversionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = YearlyLeaveConversion.objects.all()
    serializer_class = YearlyLeaveConversionSerializer
    permission_classes = [IsAuthenticated]
