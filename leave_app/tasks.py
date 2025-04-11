from celery import shared_task
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from .models import LeaveApplication, MonthlyLeaveCredit, YearlyLeaveConversion

User = get_user_model()

@shared_task
def auto_approve_leave(leave_application_id):
    try:
        leave_app = LeaveApplication.objects.get(id=leave_application_id)
        # If still pending, check if it is past the deadline.
        if leave_app.status == 'pending':
            leave_date_start = timezone.make_aware(datetime.datetime.combine(leave_app.leave_date, datetime.time.min))
            deadline = leave_date_start - datetime.timedelta(hours=24)
            if timezone.now() >= deadline:
                leave_app.status = 'auto_approved'
                leave_app.save()
    except LeaveApplication.DoesNotExist:
        pass

@shared_task
def credit_monthly_leaves():
    """
    This task credits each employee with 2 leave days for the current month.
    Should be scheduled to run on the 1st day of each month.
    """
    now = timezone.now()
    year, month = now.year, now.month
    for user in User.objects.all():
        if not MonthlyLeaveCredit.objects.filter(employee=user, year=year, month=month).exists():
            MonthlyLeaveCredit.objects.create(employee=user, year=year, month=month, credit=2.0)

@shared_task
def convert_yearly_leave():
    """
    This task calculates if an employee has more than 22 days of leave credit for the year.
    If so, extra leave days are converted into money at a predefined rate.
    Should be scheduled to run at the end of each year.
    """
    current_year = timezone.now().year
    conversion_rate = 100.0  # Example: each extra leave day converts to 100 monetary units
    for user in User.objects.all():
        # Sum credits for the year (from all months)
        total_credit = sum(MonthlyLeaveCredit.objects.filter(employee=user, year=current_year).values_list('credit', flat=True))
        if total_credit > 22:
            extra_days = total_credit - 22
            conversion_amount = extra_days * conversion_rate
            # Create conversion record if not already present.
            if not YearlyLeaveConversion.objects.filter(employee=user, year=current_year).exists():
                YearlyLeaveConversion.objects.create(
                    employee=user,
                    year=current_year,
                    extra_leaves=extra_days,
                    conversion_amount=conversion_amount
                )
