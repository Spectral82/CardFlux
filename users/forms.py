from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class RegisterForm(UserCreationForm):
    """Регистрация. Подтверждение пароля — поля password1/password2 из UserCreationForm."""

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2", "phone", "country", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label


class LoginForm(AuthenticationForm):
    """Авторизация по email и паролю."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Пароль"}
        )


class ProfileForm(forms.ModelForm):
    """Редактирование профиля. Email изменять нельзя — это логин."""

    class Meta:
        model = User
        fields = ("username", "avatar", "phone", "country")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label