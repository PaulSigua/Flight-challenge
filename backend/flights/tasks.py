from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import FlightRequest

@shared_task
def notify_owners_two_days_before():
    target_date = timezone.localdate() + timedelta(days=2)
    qs = FlightRequest.objects.filter(travel_date=target_date, status=FlightRequest.STATUS_PENDING, notified_2days=False)
    sent_ids = []
    for fr in qs.select_related("owner", "city"):
        recipient = fr.owner.email
        if not recipient:
            continue
        subject = f"Recordatorio: vuelo a {fr.city.name} el {fr.travel_date}"
        message = (
            f"Hola {fr.owner.username},\n\n"
            f"Te recordamos que tienes un vuelo a {fr.city.name} programado para {fr.travel_date}.\n"
            "Este es un recordatorio con 2 días de anticipación.\n\nSaludos."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
        fr.notified_2days = True
        fr.save(update_fields=["notified_2days"])
        sent_ids.append(fr.id)
    return {"sent_count": len(sent_ids), "ids": sent_ids}
