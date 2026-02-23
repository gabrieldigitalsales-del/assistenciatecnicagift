from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    LoginForm,
    MachineForm,
    TicketCreateForm,
    TicketMessageForm,
    PartRequestForm,
    PartRequestItemForm,
)
from .models import Machine, Ticket, TicketMedia, TicketMessage, Manual, PartRequest, PartRequestItem


def auth_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        login(request, user)
        return redirect("dashboard")

    return render(request, "auth_login.html", {"form": form})


@login_required
def auth_logout(request):
    logout(request)
    return redirect("auth_login")


@login_required
def dashboard(request):
    my_tickets_open = Ticket.objects.filter(owner=request.user).exclude(status__in=["DONE", "CANCELED"]).count()
    my_partreq_open = PartRequest.objects.filter(owner=request.user).exclude(status__in=["SENT", "CANCELED"]).count()

    ctx = {
        "my_tickets_open": my_tickets_open,
        "my_partreq_open": my_partreq_open,
    }
    return render(request, "dashboard.html", ctx)


@login_required
def machines_list(request):
    machines = Machine.objects.filter(owner=request.user).order_by("-id")
    return render(request, "machines_list.html", {"machines": machines})


@login_required
def machine_create(request):
    form = MachineForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        obj.save()
        messages.success(request, "Máquina cadastrada com sucesso.")
        return redirect("machines_list")
    return render(request, "machine_form.html", {"form": form, "mode": "create"})


@login_required
def machine_edit(request, machine_id: int):
    machine = get_object_or_404(Machine, id=machine_id, owner=request.user)
    form = MachineForm(request.POST or None, instance=machine)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Máquina atualizada.")
        return redirect("machines_list")
    return render(request, "machine_form.html", {"form": form, "mode": "edit", "machine": machine})


@login_required
def tickets_list(request):
    tickets = Ticket.objects.filter(owner=request.user).order_by("-id")
    return render(request, "tickets_list.html", {"tickets": tickets})


@login_required
def ticket_create(request):
    form = TicketCreateForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.owner = request.user
        ticket.save()

        # ✅ múltiplas mídias
        files = request.FILES.getlist("media_files")
        for f in files:
            TicketMedia.objects.create(ticket=ticket, file=f)

        messages.success(request, f"Chamado #{ticket.id} criado.")
        return redirect("ticket_detail", ticket_id=ticket.id)

    return render(request, "ticket_create.html", {"form": form})


@login_required
def ticket_detail(request, ticket_id: int):
    ticket = get_object_or_404(Ticket, id=ticket_id, owner=request.user)

    msg_form = TicketMessageForm(request.POST or None)
    if request.method == "POST" and msg_form.is_valid():
        msg = msg_form.save(commit=False)
        msg.ticket = ticket
        msg.sender_role = "CLIENT"
        msg.save()
        messages.success(request, "Mensagem enviada.")
        return redirect("ticket_detail", ticket_id=ticket.id)

    ctx = {
        "ticket": ticket,
        "media": ticket.media.all().order_by("-id"),
        "messages_list": ticket.messages.all().order_by("created_at"),
        "msg_form": msg_form,
    }
    return render(request, "ticket_detail.html", ctx)


@login_required
def manuals_list(request):
    # lista geral (se quiser filtrar por modelo depois)
    manuals = Manual.objects.filter(active=True).order_by("model__name", "title")
    return render(request, "manuals_list.html", {"manuals": manuals})


@login_required
def part_requests_list(request):
    prs = PartRequest.objects.filter(owner=request.user).order_by("-id")
    return render(request, "part_requests_list.html", {"part_requests": prs})


@login_required
def part_request_create(request):
    form = PartRequestForm(request.POST or None, user=request.user)

    # form para item (adiciona 1 por vez no MVP)
    item_form = PartRequestItemForm(request.POST or None)

    if request.method == "POST":
        # Primeiro cria o cabeçalho
        if form.is_valid():
            pr = form.save(commit=False)
            pr.owner = request.user
            pr.save()

            # se vier item na mesma tela (opcional)
            if item_form.is_valid() and item_form.cleaned_data.get("part"):
                item = item_form.save(commit=False)
                item.part_request = pr
                item.save()

            messages.success(request, f"Solicitação de peça #{pr.id} criada.")
            return redirect("part_requests_list")

    return render(
        request,
        "part_request_create.html",
        {"form": form, "item_form": item_form},
    )