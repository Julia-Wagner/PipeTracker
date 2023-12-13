from django.views.generic import CreateView
from .models import Category
from .forms import CategoryForm


class AddCategory(CreateView):
    """
    Add Category view
    """
    template_name = "stock/add_category.html"
    model = Category
    form_class = CategoryForm
    success_url = "/categories/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddCategory, self).form_valid(form)
