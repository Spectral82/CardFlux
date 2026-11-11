from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Product, ContactMessage


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        return Product.objects.filter(is_published=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsView(View):
    template_name = "catalog/contacts.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not phone or not message:
            messages.error(request, "Все поля обязательны для заполнения.")
            return render(request, self.template_name)

        ContactMessage.objects.create(name=name, phone=phone, message=message)
        messages.success(request, "Спасибо! Ваше сообщение принято.")
        return render(request, self.template_name)


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        return Product.objects.filter(is_published=True)


class OwnerRequiredMixin(UserPassesTestMixin):
    """Редактирование доступно только владельцу продукта."""
    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.owner == self.request.user


class OwnerOrModeratorRequiredMixin(UserPassesTestMixin):
    """Удаление доступно владельцу или модератору (право delete_product)."""
    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return user.is_authenticated and (
            obj.owner == user or user.has_perm("catalog.delete_product")
        )


@method_decorator(login_required, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ProductUpdateView(OwnerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})


@method_decorator(login_required, name="dispatch")
class ProductDeleteView(OwnerOrModeratorRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")


@method_decorator(login_required, name="dispatch")
class ProductUnpublishView(View):
    """Отмена публикации — только для пользователей с правом can_unpublish_product."""

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs["pk"])
        if not request.user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden("Нет права отменять публикацию продукта.")

        product.is_published = False
        product.save(update_fields=["is_published"])
        messages.success(request, f"Публикация товара «{product.name}» отменена.")
        return redirect("product_detail", pk=product.pk)