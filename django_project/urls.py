from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.campaigns.urls")),
    path("cuenta/", include("apps.accounts.urls")),
    path("donaciones/", include("apps.donations.urls")),
]

# Static/media: en local DEBUG=True; en OCI con DEBUG=False usar SERVE_MEDIA=True
if settings.DEBUG or getattr(settings, "SERVE_MEDIA", False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
