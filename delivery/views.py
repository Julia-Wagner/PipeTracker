from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .models import Note


class DeliveryNotes(ListView):
    """
    List all delivery notes
    """
    template_name = "delivery/delivery_notes.html"
    model = Note
    context_object_name = "notes"
