import django_tables2 as tables
from django.utils.html import format_html
from django.utils.timezone import localtime
from django_tables2.utils import A

from .models import Note, NoteItem


class DateColumn(tables.Column):
    """
    Render date field in desired format
    """
    def render(self, value):
        date = localtime(value).strftime("%d.%m.%Y %H:%M")
        return format_html("{}", date)


class NoteTable(tables.Table):
    """
    Delivery Notes table
    """
    date = DateColumn(verbose_name="created at")
    user = tables.Column(verbose_name="created by")
    edit = tables.TemplateColumn(template_name="delivery/edit_link.html",
                                 orderable=False)
    title = tables.LinkColumn("delivery_note_detail", args=[A("pk")],
                              verbose_name="title (click to open)",
                              attrs={"a": {"class": "font-bold text-darkblue "
                                                    "hover:text-lightblue"}})

    class Meta:
        model = Note
        template_name = "django_tables2/table.html"
        fields = ("customer", "title", "user", "date")
        row_attrs = {
            "class": lambda record: "bg-customwhite border-b hover:bg-gray-200"
            if record.status == "open" else "bg-danger bg-opacity-25 border-b "
                                            "hover:bg-gray-200"
        }


class NoteDetailsTable(tables.Table):
    """
    Delivery Note details table
    """
    quantity = tables.TemplateColumn(
        template_name="delivery/quantity_field.html", orderable=False)

    class Meta:
        model = NoteItem
        template_name = "django_tables2/table.html"
        fields = ("quantity", "item__name", "item__size", "item__matchcode",
                  "item__price")
        row_attrs = {
            "class": "bg-customwhite border-b hover:bg-gray-200"
        }
