from django.contrib import admin
from .models import LeaveType, LeaveApplication, MonthlyLeaveCredit, ApprovalLog
# Register your models here.
admin.site.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'leave_type', 'description']
    list_search = ['leave_type']
    

admin.site.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'leave_type', 'leave_date', 'duration', 'status', 'applied_at', 'updated_at']
    list_search = ['employee', 'leave_type']
    

admin.site.register(MonthlyLeaveCredit)
class MonthlyLeaveCreditAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'year', 'month', 'credit']
    list_search = ['employee', 'credit']
    

    
admin.site.register(ApprovalLog)
class ApprovalLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'leave_application', 'supervisor', 'action', 'comment']
    list_search = ['supervisor', 'action']
