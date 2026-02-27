from django.contrib import admin
from .models import (
    MachineModel,
    Machine,
    Symptom,
    Manual,
    Part,
    Ticket,
    TicketMedia,
    TicketMessage,
    PartRequest,
    PartRequestItem,
)


@admin.register(MachineModel)
class MachineModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "active")
    list_filter = ("category", "active")
    search_fields = ("name",)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "model", "serial", "city", "uf")
    list_filter = ("uf", "model")
    search_fields = ("serial", "owner__username", "model__name")


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "active")
    list_filter = ("category", "active")
    search_fields = ("title",)


@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "model", "active")
    list_filter = ("model", "active")
    search_fields = ("title",)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "active")
    list_filter = ("active",)
    search_fields = ("sku", "name")
    filter_horizontal = ("compatible_models",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "machine", "status", "priority", "created_at")
    list_filter = ("status", "priority", "category")
    search_fields = ("id", "owner__username", "machine__serial")
    ordering = ("-id",)


@admin.register(TicketMedia)
class TicketMediaAdmin(admin.ModelAdmin):
    # ✅ removido 'media_type' porque não existe no model
    list_display = ("id", "ticket", "file", "created_at")
    search_fields = ("ticket__id", "ticket__owner__username")
    ordering = ("-id",)


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "sender_role", "created_at")
    list_filter = ("sender_role",)
    search_fields = ("ticket__id", "message")
    ordering = ("-id",)


class PartRequestItemInline(admin.TabularInline):
    model = PartRequestItem
    extra = 0


@admin.register(PartRequest)
class PartRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "machine", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "owner__username", "machine__serial")
    ordering = ("-id",)
    inlines = [PartRequestItemInline]


@admin.register(PartRequestItem)
class PartRequestItemAdmin(admin.ModelAdmin):
    list_display = ("id", "part_request", "part", "qty")
    search_fields = ("part__name", "part__sku")
    ordering = ("-id",)