from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .models import Note
from .forms import NoteForm


class DeliveryNotes(ListView):
    """
    List all delivery notes
    """
    template_name = "delivery/delivery_notes.html"
    model = Note
    context_object_name = "notes"


class AddNote(CreateView):
    """
    Add delivery notes view
    """
    template_name = "delivery/add_note.html"
    model = Note
    form_class = NoteForm
    success_url = "/delivery/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddNote, self).form_valid(form)
