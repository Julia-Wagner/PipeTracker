from django.views.generic import TemplateView

from delivery.models import Note, NoteItem
from stock.models import Item


class Index(TemplateView):
    template_name = "home/index.html"


class Dashboard(TemplateView):
    template_name = "home/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get stock item numbers
        stock_items = Item.objects.all()
        stock_items_number = stock_items.count()
        stock_items_total_number = sum([item.quantity for item in stock_items])

        # get the total of all stock items
        stock_total = sum([(item.price * item.quantity)
                          for item in stock_items])

        # get the delivery note numbers
        delivery_notes = Note.objects.all()
        delivery_notes_number = delivery_notes.count()
        delivery_notes_number_open = (delivery_notes.
                                      filter(status="open").count())
        delivery_notes_number_closed = (delivery_notes.
                                        filter(status="closed").count())

        # get the total of all delivery notes
        note_items = NoteItem.objects.all()
        delivery_notes_total = (
            sum([(delivery_item.item.price * delivery_item.quantity)
                 for delivery_item in note_items]))

        context["stock_items_number"] = stock_items_number
        context["stock_items_total_number"] = stock_items_total_number
        context["stock_total"] = stock_total
        context["delivery_notes_total"] = delivery_notes_total
        context["delivery_notes_number_open"] = delivery_notes_number_open
        context["delivery_notes_number_closed"] = delivery_notes_number_closed

        return context
