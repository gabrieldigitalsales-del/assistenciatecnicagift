from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def index(request: HttpRequest) -> HttpResponse:
    # Aqui você substitui pelo seu sistema real (views/urls/templates do seu app)
    return render(request, "assistencia/index.html")