import django_tables2 as tables
from django.utils.html import format_html
from django.utils.timezone import localtime
from django_tables2.utils import A

from .models import Note, NoteItem


class DateColumn(tables.Column):
    """
    Render date field in desired format.
    """
    def render(self, value):
        """
        Render the date field in the format of 01.01.1999 09:00
        :param value:
        :return: formatted date
        """
        date = localtime(value).strftime("%d.%m.%Y %H:%M")
        return format_html("{}", date)


class NoteTable(tables.Table):
    """
    Delivery Notes table.
    """
    date = DateColumn(verbose_name="created at")
    user = tables.Column(verbose_name="created by")
    # render a template with a link for the edit cell
    edit = tables.TemplateColumn(template_name="delivery/edit_link.html",
                                 orderable=False)
    # render a link with custom classes for the title cell
    title = tables.LinkColumn("delivery_note_detail", args=[A("pk")],
                              verbose_name="title (click to open)",
                              attrs={"a": {"class": "font-bold text-darkblue "
                                                    "hover:text-lightblue"}})

    class Meta:
        model = Note
        template_name = "django_tables2/table.html"
        fields = ("customer", "title", "user", "date")
        # add custom classes to each row, depending on the status of the note
        row_attrs = {
            "class": lambda record: "bg-customwhite border-b hover:bg-gray-200"
            if record.status == "open" else "bg-danger bg-opacity-25 border-b "
                                            "hover:bg-gray-200"
        }


class NoteDetailsTable(tables.Table):
    """
    Delivery Note details table.
    """
    # render a template with buttons for the quantity cell
    quantity = tables.TemplateColumn(
        template_name="delivery/quantity_field.html", orderable=False)
    price = tables.Column(accessor="item__price", verbose_name="total")

    class Meta:
        model = NoteItem
        template_name = "django_tables2/table.html"
        fields = ("quantity", "item__name", "item__size", "item__matchcode")
        # add custom classes to each row
        row_attrs = {
            "class": "bg-customwhite border-b hover:bg-gray-200"
        }

    def render_price(self, value, record):
        """
        Render the total price for the stock item in the delivery note.
        Multiply the price with the quantity.
        :param value:
        :param record:
        :return: formatted price
        """
        return format_html("€ {}", value * record.quantity)
