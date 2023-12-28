import django_tables2 as tables
from django.utils.html import format_html
from django.utils.timezone import localtime
from django_tables2.utils import A
from .models import Note


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
    edit = tables.LinkColumn("delivery_edit_note", args=[A("pk")],
                             text="Edit", orderable=False)

    class Meta:
        model = Note
        template_name = "django_tables2/table.html"
        fields = ("customer", "title", "user", "date", "status")
