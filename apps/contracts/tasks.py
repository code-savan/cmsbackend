from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Contract

@shared_task
def check_contract_expiry():
    """
    Celery task to check for contracts nearing expiry and send email notifications.
    Runs daily to check contracts expiring in the next 7 days.
    """
    # Get contracts expiring in the next 7 days
    expiry_threshold = timezone.now() + timedelta(days=7)

    contracts = Contract.objects.filter(
        expiry_date__lte=expiry_threshold,
        expiry_date__gt=timezone.now(),
        status='active'
    )

    for contract in contracts:
        days_until_expiry = (contract.expiry_date - timezone.now()).days

        # Send email notification
        send_mail(
            subject=f'Contract Expiring Soon: {contract.title}',
            message=f'''Your contract "{contract.title}" will expire in {days_until_expiry} days.

Contract Details:
- Description: {contract.description}
- Expiry Date: {contract.expiry_date.strftime('%Y-%m-%d')}
- Status: {contract.status}

Please review and take necessary action.''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[contract.user.email],
            fail_silently=False,
        )

@shared_task
def update_expired_contracts():
    """
    Celery task to automatically update contract status to 'expired'
    when they reach their expiry date.
    """
    Contract.objects.filter(
        expiry_date__lte=timezone.now(),
        status='active'
    ).update(status='expired')
