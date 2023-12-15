from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import AddCategory, Categories, CategoriesChildren

urlpatterns = [
    path("", login_required(Categories.as_view()),
         name="categories"),
    path("categories/<int:pk>/", login_required(CategoriesChildren.as_view()),
         name="categories_children"),
    path("categories/add", login_required(AddCategory.as_view()),
         name="add_category"),
]
