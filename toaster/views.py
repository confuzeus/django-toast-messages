from django.shortcuts import HttpResponse, render
from django.contrib import messages


def alert_view(request):
    alert_level = request.GET.get("level", "info")
    messages.add_message(
        request,
        getattr(messages, alert_level.upper()),
        f"A message of level <b>{alert_level}</b>.",
    )
    return HttpResponse()
