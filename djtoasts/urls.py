"""
URL configuration for djtoasts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from toaster.views import alert_view
from django.contrib import messages
from django_htmx.http import reswap, trigger_client_event
from django.shortcuts import HttpResponse


def home(request):
    messages.info(request, "An initial message on page load.")
    return render(request, "index.html")


def toast_messages(request):
    storage = messages.get_messages(request)
    if len(storage) == 0:
        response = HttpResponse()
        return reswap(response, "none")

    response = render(request, "toasts.html")
    return trigger_client_event(response, "toasts:initialize", after="swap")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("alert/", alert_view, name="alert"),
    path("toasts/", toast_messages, name="toasts"),
    path("", home, name="home"),
]
