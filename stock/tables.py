import django_tables2 as tables
from django.utils.html import format_html
from django_tables2.utils import A
from .models import Item


class ItemTable(tables.Table):
    """
    Stock Items table.
    """
    # render a template with buttons for the quantity cell
    quantity = tables.TemplateColumn(
        template_name="stock/quantity_field.html")
    # render a template with a link for the name cell
    name = tables.LinkColumn("stock_item_detail", args=[A("pk")],
                             verbose_name="name (click to open)",
                             attrs={"a": {"class": "font-bold text-darkblue "
                                                   "hover:text-lightblue"}})
    details = tables.Column(orderable=False)
    price = tables.Column(accessor="price")
    # render a template with a link for the edit cell
    edit = tables.LinkColumn("stock_edit_item", args=[A("pk")],
                             text="Edit", orderable=False,
                             attrs={"a": {"class": "font-bold text-darkblue "
                                                   "hover:text-lightblue"}})
    # render a template with a form for the basket cell
    basket = tables.TemplateColumn(template_name="stock/basket_quantity.html",
                                   orderable=False,
                                   verbose_name="Add to basket")

    class Meta:
        model = Item
        template_name = "django_tables2/table.html"
        fields = ("quantity", "name", "size", "matchcode", "details", "price")
        # add custom classes to each row
        row_attrs = {
            "class": "bg-customwhite border-b hover:bg-gray-200"
        }

    def render_price(self, value):
        """
        Render the price for the stock item.
        :param value:
        :return: formatted price
        """
        return format_html("€ {}", value)
