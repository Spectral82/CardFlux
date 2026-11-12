from django.contrib import admin

from .models import Category, Product, ContactMessage, ContactData


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active", "is_published", "owner")
    list_filter = ("is_active", "is_published", "category")
    search_fields = ("name", "description")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at")
    readonly_fields = ("name", "phone", "message", "created_at")


@admin.register(ContactData)
class ContactDataAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "is_active")
    list_filter = ("is_active",)