from django import forms
from django.contrib.auth import authenticate

from .models import (
    Machine,
    Ticket,
    TicketMessage,
    PartRequest,
    PartRequestItem,
    Part,
    Symptom,
)


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuário"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"}),
    )

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("username")
        password = cleaned.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuário ou senha inválidos.")
            cleaned["user"] = user
        return cleaned


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ["model", "serial", "city", "uf", "purchase_date", "notes"]
        widgets = {
            "model": forms.Select(attrs={"class": "form-select"}),
            "serial": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "uf": forms.TextInput(attrs={"class": "form-control", "maxlength": 2}),
            "purchase_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class TicketCreateForm(forms.ModelForm):
    media_files = forms.FileField(
        label="Fotos/Vídeos (opcional)",
        required=False,
        widget=MultipleFileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Ticket
        fields = ["machine", "category", "symptom", "priority", "description"]
        widgets = {
            "machine": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "symptom": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # filtra máquina do dono
        if user:
            self.fields["machine"].queryset = Machine.objects.filter(owner=user).order_by("-id")

        # sintomas ativos
        self.fields["symptom"].queryset = Symptom.objects.filter(active=True).order_by("title")


class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Digite sua mensagem..."}
            ),
        }


class PartRequestForm(forms.ModelForm):
    class Meta:
        model = PartRequest
        fields = [
            "machine",
            "contact_name",
            "contact_phone",
            "shipping_name",
            "shipping_cpf_cnpj",
            "shipping_zip",
            "shipping_address",
            "shipping_number",
            "shipping_complement",
            "shipping_neighborhood",
            "shipping_city",
            "shipping_uf",
            "notes",
        ]
        widgets = {
            "machine": forms.Select(attrs={"class": "form-select"}),
            "contact_name": forms.TextInput(attrs={"class": "form-control"}),
            "contact_phone": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_name": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_cpf_cnpj": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_zip": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_address": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_number": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_complement": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_neighborhood": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_city": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_uf": forms.TextInput(attrs={"class": "form-control", "maxlength": 2}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["machine"].queryset = Machine.objects.filter(owner=user).order_by("-id")


class PartRequestItemForm(forms.ModelForm):
    class Meta:
        model = PartRequestItem
        fields = ["part", "qty", "notes"]
        widgets = {
            "part": forms.Select(attrs={"class": "form-select"}),
            "qty": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "notes": forms.TextInput(attrs={"class": "form-control", "placeholder": "Opcional"}),
        }

    def __init__(self, *args, **kwargs):
        machine = kwargs.pop("machine", None)
        super().__init__(*args, **kwargs)

        qs = Part.objects.filter(active=True).order_by("name")
        # Se quiser filtrar por compatibilidade de modelo:
        if machine and machine.model_id:
            qs = qs.filter(compatible_models=machine.model).distinct().order_by("name")

        self.fields["part"].queryset = qs