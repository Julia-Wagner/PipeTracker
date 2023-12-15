from django.views.generic import CreateView, ListView
from .models import Category
from .forms import CategoryForm


class Categories(ListView):
    """
    List all categories
    """
    template_name = "stock/categories.html"
    model = Category
    context_object_name = "categories"


class AddCategory(CreateView):
    """
    Add Category view
    """
    template_name = "stock/add_category.html"
    model = Category
    form_class = CategoryForm
    success_url = "/stock/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddCategory, self).form_valid(form)
