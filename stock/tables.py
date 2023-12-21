import django_tables2 as tables
from .models import Item


class ItemTable(tables.Table):
    """
    Stock Items table
    """
    class Meta:
        model = Item
        fields = ("name", "size", "matchcode", "price", "quantity")
