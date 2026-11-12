import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from CardFlux import settings
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import User

logger = logging.getLogger(__name__)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        try:
            user = form.save()
        except Exception:
            logger.exception("Ошибка при создании пользователя")
            messages.error(
                self.request,
                "Не удалось создать аккаунт. Попробуйте ещё раз.",
            )
            return self.form_invalid(form)

        # Приветственное письмо
        try:
            send_mail(
                subject="Добро пожаловать в CardFlux!",
                message=(
                    f"Здравствуйте, {user.username}!\n\n"
                    "Спасибо за регистрацию в CardFlux.\n"
                    "Теперь вы можете просматривать каталог и управлять товарами."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Не удалось отправить приветственное письмо")
            messages.warning(
                self.request,
                "Аккаунт создан, но приветственное письмо не отправилось.",
            )

        login(self.request, user, backend="users.backends.EmailBackend")
        messages.success(self.request, "Регистрация прошла успешно!")
        return redirect(self.success_url)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, "Вы вошли в аккаунт.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Неверный email или пароль.")
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        # Профиль редактируем только свой
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлён.")
        return super().form_valid(form)