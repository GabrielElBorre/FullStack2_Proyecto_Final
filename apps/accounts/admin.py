from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .admin_forms import CustomUserAdminChangeForm, CustomUserAdminCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserAdminChangeForm
    add_form = CustomUserAdminCreationForm

    list_display = ("email", "first_name", "last_name", "rol", "is_staff", "is_active")
    list_filter = ("rol", "is_staff", "is_active")
    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name")}),
        ("Rol y permisos", {"fields": ("rol", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2", "rol"),
            },
        ),
    )
