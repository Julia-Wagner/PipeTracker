from django.views.generic import CreateView, ListView, UpdateView
from django_tables2 import RequestConfig
from django.shortcuts import redirect
from .models import Note
from .forms import NoteForm
from .tables import NoteTable


class DeliveryNotes(ListView):
    """
    List all delivery notes
    """
    template_name = "delivery/delivery_notes.html"
    model = Note
    context_object_name = "notes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        notes = Note.objects.all()

        # create and configure stock items table
        table = NoteTable(notes)
        RequestConfig(self.request).configure(table)

        # create delivery notes dictionary
        notes_dic = []
        for row in table.rows:
            note_dic = {}
            for column, cell in row.items():
                # use verbose name for heading
                note_dic[column.verbose_name] = cell
            notes_dic.append(note_dic)

        context["table"] = table
        context["notes_dic"] = notes_dic

        return context


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


class EditNote(UpdateView):
    """
    Edit a delivery note
    """
    template_name = "delivery/edit_note.html"
    model = Note
    form_class = NoteForm
    success_url = "/delivery/"

    # don´t allow editing for closed notes
    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()

        if note.status == "closed":
            return redirect("/delivery/")

        # call parent dispatch method
        return super().dispatch(request, *args, **kwargs)
