from django.views.generic import CreateView, TemplateView
from .models import Category
from .forms import CategoryForm


class Categories(TemplateView):
    template_name = "stock/categories.html"


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
