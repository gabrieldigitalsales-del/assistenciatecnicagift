from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sobre/", views.about, name="about"),
    path("maquinas/", views.machines, name="machines"),
    path("maquinas/<slug:slug>/", views.machine_detail, name="machine_detail"),
    path("contato/", views.contact, name="contact"),
    path("solicitar-orcamento/", views.request_quote, name="request_quote"),
]