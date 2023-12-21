import django_tables2 as tables
from .models import Item


class ItemTable(tables.Table):
    """
    Stock Items table
    """
    class Meta:
        model = Item
        template_name = "django_tables2/table.html"
        fields = ("name", "size", "matchcode", "details", "price", "quantity")
