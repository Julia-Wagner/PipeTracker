from django.contrib import admin
from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "image_alt", "parent", "order")
    search_fields = ["name"]
    prepopulated_fields = {"image_alt": ("name",)}
    list_filter = ("parent",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "matchcode", "price", "quantity",
                    "size", "details")
    search_fields = ["name", "category", "matchcode", "size"]
    list_filter = ("category",)
