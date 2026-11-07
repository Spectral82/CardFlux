from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View

from .models import Product, ContactMessage


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


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