from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_notification_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        "your_email@example.com",
        [to_email],
        fail_silently=False,
    )
