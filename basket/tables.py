import django_tables2 as tables
from .models import BasketItem


class BasketTable(tables.Table):
    """
    Basket table
    """

    class Meta:
        model = BasketItem
        template_name = "django_tables2/table.html"
        fields = ("quantity", "item__name", "item__size", "item__matchcode",
                  "item__details")
