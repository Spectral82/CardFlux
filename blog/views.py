import logging

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import BlogPost

logger = logging.getLogger(__name__)


class BlogEditorRequiredMixin(UserPassesTestMixin):
    """Работать с блогом может только контент-менеджер или суперпользователь."""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_superuser or user.has_perm("blog.change_blogpost")
        )


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])

        # Поздравление при достижении 100 просмотров.
        # Строгая проверка на 100, чтобы письмо не улетало на каждый просмотр после.
        if obj.views_count == 100:
            try:
                send_mail(
                    subject=f"Пост «{obj.title}» набрал 100 просмотров!",
                    message=(
                        f"Поздравляем!\n\n"
                        f"Статья «{obj.title}» достигла 100 просмотров.\n"
                        f"Всего просмотров сейчас: {obj.views_count}."
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except Exception:
                logger.exception("Не удалось отправить поздравление о 100 просмотрах")

        return obj


class BlogPostCreateView(BlogEditorRequiredMixin, CreateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blogpost_list")


class BlogPostUpdateView(BlogEditorRequiredMixin, UpdateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        return reverse("blogpost_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(BlogEditorRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blogpost_list")