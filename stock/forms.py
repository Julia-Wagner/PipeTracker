import csv

from django import forms
from .models import Category, Item
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError


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

    # ensure no subcategories can be added to categories with linked items
    # https://docs.djangoproject.com/en/5.0/ref/forms/validation/#validating-fields-with-clean
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("parent")

        if category and Item.objects.filter(category=category).exists():
            raise ValidationError(
                "Can not add subcategories to a category with stock items.")

        return cleaned_data

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


class ItemForm(forms.ModelForm):
    """
    Form to create a Stock Item
    """

    def __init__(self, *args, **kwargs):
        """
        Add custom classes to the form.
        """
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "block mb-2 text-customblack font-bold"
        self.helper.form_tag = False

        # only show categories with no subcategories
        self.fields["category"].queryset = (
            Category.objects.filter(children__isnull=True))

    class Meta:
        model = Item
        fields = ["name", "category", "matchcode", "price", "quantity",
                  "size", "details"]

        labels = {
            "name": "Item Name",
            "category": "Item Category",
            "matchcode": "Item matchcode",
            "price": "Price",
            "quantity": "Quantity",
            "size": "Size",
            "details": "Details",
        }


class UploadForm(forms.Form):
    """
    Form to upload a CSV file
    """

    def __init__(self, *args, **kwargs):
        """
        Add custom classes to the form.
        """
        super(UploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "block mb-2 text-customblack font-bold"
        self.helper.form_tag = False

    file = forms.FileField(
        label="CSV File",
        help_text="Upload a CSV file.",
        widget=forms.ClearableFileInput(attrs={"accept": "text/csv"})
    )

    def clean_file(self):
        csv_file = self.cleaned_data["file"]
        try:
            decoded_file = csv_file.read().decode("utf-8")
            csv.DictReader(decoded_file)
        except Exception as e:
            raise ValidationError("Please upload a valid CSV file.")

        return csv_file
