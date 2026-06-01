from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("registro/", views.SignUpView.as_view(), name="signup"),
    path("iniciar-sesion/", views.LoginView.as_view(), name="login"),
    path("cerrar-sesion/", views.LogoutView.as_view(), name="logout"),
    path("cambiar-contrasena/", views.PasswordChangeView.as_view(), name="password_change"),
    path(
        "cambiar-contrasena/listo/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("restablecer/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "restablecer/enviado/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "restablecer/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "restablecer/completado/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
