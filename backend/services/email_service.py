from django.core.mail import send_mail
from django.conf import settings

def send_plain_email(subject: str, message: str, recipients: list):
    if not recipients:
        return False
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
    return True
