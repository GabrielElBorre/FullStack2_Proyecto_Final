from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserAdminChangeForm(UserChangeForm):
    """Formulario de admin sin fallo por username=None (login por email)."""

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            self.fields["username"].required = False
            self.fields["username"].help_text = "Opcional. Se usa el correo si se deja vacío."

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username is None or username == "":
            return self.instance.email or ""
        return username


class CustomUserAdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "last_name", "rol")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user
