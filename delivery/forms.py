from django import forms
from .models import Note
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError


class NoteForm(forms.ModelForm):
    """
    Form to create a delivery note
    """

    def __init__(self, *args, **kwargs):
        """
        Add custom classes to the form.
        """
        super(NoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "block mb-2 text-customblack font-bold"
        self.helper.form_tag = False

    class Meta:
        model = Note
        fields = ["customer", "title", "status"]

        labels = {
            "customer": "Customer",
            "title": "Title",
            "status": "Status"
        }
