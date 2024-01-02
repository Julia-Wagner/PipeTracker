import django_tables2 as tables
from django_tables2.utils import A
from .models import Item


class ItemTable(tables.Table):
    """
    Stock Items table
    """
    details = tables.Column(orderable=False)
    edit = tables.LinkColumn("stock_edit_item", args=[A("pk")],
                             text="Edit", orderable=False,
                             verbose_name="action",
                             attrs={"a": {"class": "font-bold text-darkblue "
                                                   "hover:text-lightblue"}})

    class Meta:
        model = Item
        template_name = "django_tables2/table.html"
        fields = ("name", "size", "matchcode", "details", "price", "quantity",
                  "edit")
