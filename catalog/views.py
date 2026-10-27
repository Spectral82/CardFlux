from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib import messages


def product_list(request):
    products = Product.objects.all()
    return render(request, "catalog/product_list.html", {"products": products})


def home(request):
    products = Product.objects.order_by("-created_at")[:5]
    return render(request, "catalog/home.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


def contacts(request):
    """Страница контактов и обработка формы обратной связи."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not name or not phone or not message_text:
            messages.error(request, "Все поля обязательны для заполнения.")
            return render(request, "catalog/contacts.html")

        messages.success(request, "Спасибо! Ваше сообщение принято.")
        return render(request, "catalog/contacts.html")

    return render(request, "catalog/contacts.html")