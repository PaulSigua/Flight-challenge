from django.db import transaction
from .models import FlightRequest

def reserve_flight_request(fr: FlightRequest, operator_user):
    """
    Marca una FlightRequest como RESERVED de forma segura.
    Lanza ValueError si no puede.
    """
    if not operator_user.is_staff:
        raise PermissionError("Usuario no es operador.")

    with transaction.atomic():
        fr = FlightRequest.objects.select_for_update().get(pk=fr.pk)
        if fr.status != FlightRequest.STATUS_PENDING:
            raise ValueError("Solo solicitudes pendientes pueden ser reservadas.")
        fr.status = FlightRequest.STATUS_RESERVED
        fr.save(update_fields=["status", "updated_at"])
        return fr
