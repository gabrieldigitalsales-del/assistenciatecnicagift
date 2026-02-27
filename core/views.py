from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Machine

def _wa_link(text: str) -> str:
    num = getattr(settings, "WHATSAPP_NUMBER", "")
    return f"https://wa.me/{num}?text={quote(text)}" if num else "#"

def home(request: HttpRequest) -> HttpResponse:
    featured = Machine.objects.filter(is_featured=True)[:6]
    machines = Machine.objects.all()[:6]
    return render(request, "core/home.html", {"featured": featured, "machines": machines})

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html")

def machines(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q", "").strip()
    qs = Machine.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, "core/machines.html", {"machines": qs, "q": q})

def machine_detail(request: HttpRequest, slug: str) -> HttpResponse:
    machine = get_object_or_404(Machine, slug=slug)
    wa = _wa_link(
        f"Olá! Quero solicitar orçamento da máquina: {machine.name}. "
        f"Minha empresa é: ____ / Cidade: ____ / Volume de produção: ____"
    )
    return render(request, "core/machine_detail.html", {"machine": machine, "wa_link": wa})

def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")

def request_quote(request: HttpRequest) -> HttpResponse:
    # Sem envio de email agora: envia pro WhatsApp com uma mensagem bem formatada.
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        company = (request.POST.get("company") or "").strip()
        city = (request.POST.get("city") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        need = (request.POST.get("need") or "").strip()
        machine = (request.POST.get("machine") or "").strip()

        text = (
            "📌 *Solicitação de Orçamento*\n"
            f"• Nome: {name}\n"
            f"• Empresa: {company}\n"
            f"• Cidade: {city}\n"
            f"• Telefone: {phone}\n"
            f"• Máquina/Interesse: {machine}\n"
            f"• Necessidade: {need}\n"
        )

        if not name or not phone:
            messages.error(request, "Preencha pelo menos Nome e Telefone/WhatsApp.")
            return redirect("request_quote")

        return redirect(_wa_link(text))

    machines = Machine.objects.all()
    return render(request, "core/request_quote.html", {"machines": machines})