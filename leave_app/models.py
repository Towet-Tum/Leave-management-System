import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

# -----------------------------
# Leave Management Service
# -----------------------------

class LeaveType(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('vacation', 'Vacation'),
        ('sick', 'Sick'),
        ('travel', 'Travel')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.leave_type

class LeaveApplication(models.Model):
    DURATION_CHOICES = [
        ('half-day', 'Half Day'),
        ('full-day', 'Full Day'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
        ('auto_approved', 'Auto Approved'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, related_name='applications')
    leave_date = models.DateField()
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_date} ({self.duration})"

class MonthlyLeaveCredit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='monthly_credits')
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    credit = models.DecimalField(max_digits=4, decimal_places=2, default=2.0)

    class Meta:
        unique_together = ('employee', 'year', 'month')

    def __str__(self):
        return f"{self.employee} - {self.month}/{self.year} : {self.credit} days"

# -----------------------------
# Approval & Workflow Service
# -----------------------------

class ApprovalLog(models.Model):
    ACTION_CHOICES = [
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
        ('auto_approved', 'Auto Approved'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leave_application = models.ForeignKey(LeaveApplication, on_delete=models.CASCADE, related_name='approval_logs')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approval_actions')
    action = models.CharField(max_length=15, choices=ACTION_CHOICES)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.leave_application} - {self.action} by {self.supervisor}"

# -----------------------------
# Leave Conversion (Financial) Service
# -----------------------------

class YearlyLeaveConversion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_conversions')
    year = models.PositiveIntegerField()
    extra_leaves = models.DecimalField(max_digits=5, decimal_places=2)
    conversion_amount = models.DecimalField(max_digits=10, decimal_places=2)
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'year')

    def __str__(self):
        return f"{self.employee} - {self.year}: {self.extra_leaves} days -> {self.conversion_amount}"
