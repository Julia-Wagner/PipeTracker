from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import AddCategory, Categories

urlpatterns = [
    path("", login_required(Categories.as_view()),
         name="categories"),
    path("categories/add", login_required(AddCategory.as_view()),
         name="add_category"),
]
