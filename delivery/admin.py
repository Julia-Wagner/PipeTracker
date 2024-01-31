from django.contrib import admin
from .models import Customer, Note, NoteItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("number", "first_name", "last_name")
    search_fields = ["number", "first_name", "last_name"]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("customer", "title", "status", "get_items_display", "date")
    search_fields = ["customer", "title"]
    list_filter = ("status",)

    def get_items_display(self, obj):
        """
        Display the items in the note as a comma-separated list.
        :param obj:
        :return: a comma-separated list
        """
        return ", ".join([str(item) for item in obj.items.all()])

    get_items_display.short_description = "Items"


@admin.register(NoteItem)
class NoteItemAdmin(admin.ModelAdmin):
    list_display = ("note", "item", "quantity")
    search_fields = ["note__title", "item__name"]
    list_filter = ("note", "item",)
