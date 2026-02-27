from django.conf import settings
from django.db import models


class MachineModel(models.Model):
    CATEGORY_CORTE = "CORTE"
    CATEGORY_PRENSA = "PRENSA"
    CATEGORY_BATER_FUMO = "BATER_FUMO"
    CATEGORY_ELETRICA = "ELETRICA"
    CATEGORY_OUTROS = "OUTROS"

    CATEGORY_CHOICES = [
        (CATEGORY_CORTE, "Corte"),
        (CATEGORY_PRENSA, "Prensa"),
        (CATEGORY_BATER_FUMO, "Bater fumo"),
        (CATEGORY_ELETRICA, "Elétrica"),
        (CATEGORY_OUTROS, "Outros"),
    ]

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_OUTROS)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]
        verbose_name = "Modelo de Máquina"
        verbose_name_plural = "Modelos de Máquina"

    def __str__(self):
        return self.name


class Machine(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="machines",
    )
    model = models.ForeignKey(
        MachineModel,
        on_delete=models.PROTECT,
        related_name="machines",
    )
    serial = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"
        indexes = [
            models.Index(fields=["owner", "model"]),
            models.Index(fields=["serial"]),
        ]

    def __str__(self):
        serial_txt = self.serial or "s/serial"
        return f"{self.model.name} ({serial_txt})"


class Symptom(models.Model):
    CATEGORY_CHOICES = MachineModel.CATEGORY_CHOICES

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=MachineModel.CATEGORY_OUTROS)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "title"]
        verbose_name = "Sintoma"
        verbose_name_plural = "Sintomas"

    def __str__(self):
        return self.title


class Manual(models.Model):
    model = models.ForeignKey(MachineModel, on_delete=models.CASCADE, related_name="manuals")
    title = models.CharField(max_length=160)
    file = models.FileField(upload_to="manuals/", blank=True, null=True)
    url = models.URLField(blank=True)  # link drive/youtube/etc
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["model__name", "title"]
        verbose_name = "Manual"
        verbose_name_plural = "Manuais"

    def __str__(self):
        return self.title


class Part(models.Model):
    sku = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    # compatibilidade por modelo
    compatible_models = models.ManyToManyField(
        MachineModel,
        blank=True,
        related_name="compatible_parts",
    )

    class Meta:
        ordering = ["sku"]
        verbose_name = "Peça"
        verbose_name_plural = "Peças"
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Ticket(models.Model):
    STATUS_OPEN = "OPEN"
    STATUS_TRIAGE = "TRIAGE"
    STATUS_WAITING = "WAITING"
    STATUS_QUOTE = "QUOTE"
    STATUS_SENT = "SENT"
    STATUS_DONE = "DONE"
    STATUS_CANCELED = "CANCELED"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Aberto"),
        (STATUS_TRIAGE, "Em triagem"),
        (STATUS_WAITING, "Aguardando cliente"),
        (STATUS_QUOTE, "Orçamento"),
        (STATUS_SENT, "Enviado"),
        (STATUS_DONE, "Finalizado"),
        (STATUS_CANCELED, "Cancelado"),
    ]

    PRIORITY_LOW = "LOW"
    PRIORITY_MEDIUM = "MEDIUM"
    PRIORITY_HIGH = "HIGH"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Baixa"),
        (PRIORITY_MEDIUM, "Média"),
        (PRIORITY_HIGH, "Alta"),
    ]

    CATEGORY_CHOICES = MachineModel.CATEGORY_CHOICES

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, related_name="tickets")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=MachineModel.CATEGORY_OUTROS)
    symptom = models.ForeignKey(Symptom, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets")
    description = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_OPEN)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["machine", "status"]),
        ]

    def __str__(self):
        return f"Chamado #{self.id}"


class TicketMedia(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="tickets/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Mídia do Chamado"
        verbose_name_plural = "Mídias do Chamado"

    def __str__(self):
        return f"Mídia #{self.id} do Ticket #{self.ticket_id}"


class TicketMessage(models.Model):
    SENDER_CLIENT = "CLIENT"
    SENDER_ADMIN = "ADMIN"
    SENDER_CHOICES = [
        (SENDER_CLIENT, "Cliente"),
        (SENDER_ADMIN, "Empresa"),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    sender_role = models.CharField(max_length=10, choices=SENDER_CHOICES, default=SENDER_CLIENT)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Mensagem do Chamado"
        verbose_name_plural = "Mensagens do Chamado"

    def __str__(self):
        return f"Msg #{self.id} Ticket #{self.ticket_id}"


class PartRequest(models.Model):
    STATUS_OPEN = "OPEN"
    STATUS_ANALYSIS = "ANALYSIS"
    STATUS_QUOTED = "QUOTED"
    STATUS_SENT = "SENT"
    STATUS_CANCELED = "CANCELED"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Aberto"),
        (STATUS_ANALYSIS, "Em análise"),
        (STATUS_QUOTED, "Orçado"),
        (STATUS_SENT, "Enviado"),
        (STATUS_CANCELED, "Cancelado"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="part_requests")
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, related_name="part_requests")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_OPEN)

    contact_name = models.CharField(max_length=120)
    contact_phone = models.CharField(max_length=40)

    shipping_name = models.CharField(max_length=120)
    shipping_cpf_cnpj = models.CharField(max_length=40, blank=True)
    shipping_zip = models.CharField(max_length=20)
    shipping_address = models.CharField(max_length=160)
    shipping_number = models.CharField(max_length=20, blank=True)
    shipping_complement = models.CharField(max_length=80, blank=True)
    shipping_neighborhood = models.CharField(max_length=80, blank=True)
    shipping_city = models.CharField(max_length=80)
    shipping_uf = models.CharField(max_length=2)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Solicitação de Peça"
        verbose_name_plural = "Solicitações de Peça"
        indexes = [
            models.Index(fields=["owner", "status"]),
        ]

    def __str__(self):
        return f"Solicitação de Peça #{self.id}"


class PartRequestItem(models.Model):
    part_request = models.ForeignKey(PartRequest, on_delete=models.CASCADE, related_name="items")
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    notes = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Item da Solicitação"
        verbose_name_plural = "Itens da Solicitação"

    def __str__(self):
        return f"{self.qty}x {self.part.name}"