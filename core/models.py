from django.db import models
from django.urls import reverse


class Machine(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=220, blank=True)
    description = models.TextField(blank=True)

    capacity = models.CharField(max_length=120, blank=True)
    power = models.CharField(max_length=120, blank=True)
    dimensions = models.CharField(max_length=140, blank=True)
    warranty = models.CharField(max_length=120, blank=True)

    image = models.ImageField(upload_to="machines/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("machine_detail", kwargs={"slug": self.slug})


# =============================
# CONFIGURAÇÕES DO SITE (ADMIN)
# =============================

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120, default="GIFT Excellence")
    site_tagline = models.CharField(max_length=200, blank=True)

    whatsapp_number = models.CharField(
        max_length=30,
        blank=True,
        help_text="Somente números com DDI. Ex: 5531999999999",
    )

    contact_phone = models.CharField(max_length=40, blank=True)
    contact_email = models.EmailField(blank=True)

    address_text = models.CharField(max_length=220, blank=True)
    google_maps_embed_url = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configurações do Site"
        verbose_name_plural = "Configurações do Site"

    def __str__(self):
        return "Configurações do Site"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj