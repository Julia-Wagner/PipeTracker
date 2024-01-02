from django.contrib import admin
from .models import Basket, BasketItem


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user", "get_items_display", "date")

    def get_items_display(self, obj):
        return ", ".join([str(item) for item in obj.items.all()])

    get_items_display.short_description = "Items"


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ("basket", "item", "quantity")
    search_fields = ["basket__user__username", "item__name"]
    list_filter = ("basket", "item",)
