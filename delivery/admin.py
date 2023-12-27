from django.contrib import admin
from .models import Customer, Note


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("number", "first_name", "last_name")
    search_fields = ["number", "first_name", "last_name"]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("customer", "title", "status", "date")
    search_fields = ["customer", "title"]
    list_filter = ("status",)
