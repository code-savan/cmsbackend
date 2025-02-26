import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('contract_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Add this configuration
app.conf.broker_connection_retry_on_startup = True

# Auto-discover tasks in all registered Django apps
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'check-contract-expiry': {
        'task': 'apps.contracts.tasks.check_contract_expiry',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
    'update-expired-contracts': {
        'task': 'apps.contracts.tasks.update_expired_contracts',
        'schedule': crontab(hour='*/1'),  # Run every hour
    },
}
