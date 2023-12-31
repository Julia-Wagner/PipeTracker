from django import forms
from .models import Note, Customer
from crispy_forms.helper import FormHelper


class CustomerForm(forms.ModelForm):
    """
    Form to create a customer
    """

    def __init__(self, *args, **kwargs):
        """
        Add custom classes to the form.
        """
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "block mb-2 text-customblack font-bold"
        self.helper.form_tag = False

    class Meta:
        model = Customer
        fields = ["number", "first_name", "last_name"]

        labels = {
            "number": "Customer number",
            "first_name": "First name",
            "last_name": "Last name"
        }


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
            "customer": "Choose an existing Customer",
            "title": "Title",
            "status": "Status"
        }
