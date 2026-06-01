from django.contrib import admin

from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("nombre", "meta_recaudacion", "recaudado_actual", "activa", "creador", "fecha_creacion")
    list_filter = ("activa", "fecha_creacion")
    search_fields = ("nombre", "descripcion")
    readonly_fields = ("recaudado_actual", "fecha_creacion")
