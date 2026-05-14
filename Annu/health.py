"""Liveness/readiness for orchestrators and observability probes."""

from django.db import connection
from django.http import JsonResponse


def health_live(_request):
    return JsonResponse({'status': 'ok', 'service': 'django'})


def health_ready(_request):
    try:
        connection.ensure_connection()
    except Exception as exc:
        return JsonResponse({'status': 'unready', 'database': str(exc)}, status=503)
    return JsonResponse({'status': 'ready', 'database': 'ok'})
