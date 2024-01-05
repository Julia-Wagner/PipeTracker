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
    basket = tables.TemplateColumn(template_name="stock/basket_quantity.html",
                                   orderable=False,
                                   verbose_name="Add to basket")

    class Meta:
        model = Item
        template_name = "django_tables2/table.html"
        fields = ("quantity", "name", "size", "matchcode", "details", "price")
        row_attrs = {
            "class": "bg-customwhite border-b hover:bg-gray-200"
        }
