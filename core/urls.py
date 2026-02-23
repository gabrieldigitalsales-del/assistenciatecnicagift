from django.urls import path

from .views import (
    auth_login,
    auth_logout,
    dashboard,
    machines_list,
    machine_create,
    machine_edit,
    tickets_list,
    ticket_create,
    ticket_detail,
    manuals_list,
    part_requests_list,
    part_request_create,
)

urlpatterns = [
    path("login/", auth_login, name="auth_login"),
    path("logout/", auth_logout, name="auth_logout"),

    path("", dashboard, name="dashboard"),

    path("machines/", machines_list, name="machines_list"),
    path("machines/new/", machine_create, name="machine_create"),
    path("machines/<int:machine_id>/edit/", machine_edit, name="machine_edit"),

    path("tickets/", tickets_list, name="tickets_list"),
    path("tickets/new/", ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/", ticket_detail, name="ticket_detail"),

    path("manuals/", manuals_list, name="manuals_list"),

    path("parts/requests/", part_requests_list, name="part_requests_list"),
    path("parts/requests/new/", part_request_create, name="part_request_create"),
]