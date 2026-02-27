from django.conf import settings
from .models import SiteSettings


def site_defaults(request):
    try:
        s = SiteSettings.get_solo()

        return {
            "SITE_NAME": s.site_name or settings.SITE_NAME,
            "SITE_TAGLINE": s.site_tagline or settings.SITE_TAGLINE,
            "WHATSAPP_NUMBER": s.whatsapp_number or settings.WHATSAPP_NUMBER,
            "CONTACT_EMAIL": s.contact_email or settings.CONTACT_EMAIL,
            "ADDRESS_TEXT": s.address_text or settings.ADDRESS_TEXT,
            "GOOGLE_MAPS_EMBED_URL": s.google_maps_embed_url or settings.GOOGLE_MAPS_EMBED_URL,
        }

    except:
        # fallback caso tabela ainda não exista
        return {
            "SITE_NAME": settings.SITE_NAME,
            "SITE_TAGLINE": settings.SITE_TAGLINE,
            "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
            "CONTACT_EMAIL": settings.CONTACT_EMAIL,
            "ADDRESS_TEXT": settings.ADDRESS_TEXT,
            "GOOGLE_MAPS_EMBED_URL": settings.GOOGLE_MAPS_EMBED_URL,
        }