from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "image_alt", "parent", "order")
    search_fields = ["name"]
    prepopulated_fields = {"image_alt": ("name",)}
    list_filter = ("parent",)
