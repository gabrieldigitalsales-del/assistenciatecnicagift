from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ Assistência técnica PRIMEIRO (pra não ser engolida pelo core.urls)
    path("assistencia/", include(("assistencia_app.urls", "assistencia"), namespace="assistencia")),

    # Site institucional
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)