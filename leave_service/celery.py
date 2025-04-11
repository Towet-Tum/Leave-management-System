import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leave_service.settings')  # Replace myproject with your project name

app = Celery('leave_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
