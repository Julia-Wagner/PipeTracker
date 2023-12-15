from django import forms
from .models import Category
from crispy_forms.helper import FormHelper


class CategoryForm(forms.ModelForm):
    """
    Form to create a Category
    """

    def __init__(self, *args, **kwargs):
        """
        Add custom classes to the form.
        """
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "block mb-2 text-customblack font-bold"
        self.helper.form_tag = False
        self.fields['image'].widget.attrs.update(
            {"class": "bg-gray-50 border border-darkblue text-gray-900 "
                      "text-sm rounded-lg focus:ring-blue-500 "
                      "focus:border-blue-500 block w-full p-2.5"})

    class Meta:
        model = Category
        fields = ["name", "image", "image_alt", "parent", "order"]

        labels = {
            "name": "Category Name",
            "image": "Category Image",
            "image_alt": "Image Description",
            "parent": "Parent Category",
            "order": "Order",
        }
