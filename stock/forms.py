from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """
    Form to create a Category
    """
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
