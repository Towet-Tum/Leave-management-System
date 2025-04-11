from rest_framework import serializers
from django.utils import timezone
import datetime
from decimal import Decimal
from django.db import transaction
from .models import (
    LeaveType,
    LeaveApplication,
    MonthlyLeaveCredit,
    ApprovalLog,
    YearlyLeaveConversion,
)

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = '__all__'
        read_only_fields = ['status', 'applied_at', 'updated_at']

    def validate_leave_date(self, value):
        # Ensure leave_date is not in the past.
        if value < timezone.localdate():
            raise serializers.ValidationError("Leave date cannot be in the past.")
        return value

    def create(self, validated_data):
        employee = validated_data.get('employee')
        leave_date = validated_data.get('leave_date')
        duration = validated_data.get('duration')

        # Determine deduction amount as a Decimal.
        deduction = Decimal('0.5') if duration == 'half-day' else Decimal('1.0')

        year = leave_date.year
        month = leave_date.month
        credit_record = MonthlyLeaveCredit.objects.filter(employee=employee, year=year, month=month).first()
        if not credit_record:
            raise serializers.ValidationError("No leave credit record found for the selected month.")
        if credit_record.credit < deduction:
            raise serializers.ValidationError("Insufficient leave credit for this leave application.")

        with transaction.atomic():
            credit_record.credit -= deduction
            credit_record.save()
            leave_app = LeaveApplication.objects.create(**validated_data)
        return leave_app

class MonthlyLeaveCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyLeaveCredit
        fields = '__all__'

class ApprovalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalLog
        fields = '__all__'

class YearlyLeaveConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearlyLeaveConversion
        fields = '__all__'
