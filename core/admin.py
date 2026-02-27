from django.contrib import admin
from .models import Machine, SiteSettings


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "is_featured", "order")
    list_editable = ("is_featured", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "short_description", "description")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "contact_phone", "contact_email", "whatsapp_number", "updated_at")

    def has_add_permission(self, request):
        # impede criar vários registros
        return False