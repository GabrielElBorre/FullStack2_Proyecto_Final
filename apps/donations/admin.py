from django.contrib import admin

from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("campana", "usuario", "monto", "fecha_donacion")
    list_filter = ("fecha_donacion",)
    search_fields = ("usuario__email", "campana__nombre")
