from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (AddCategory, Categories, CategoriesChildren,
                    DeleteCategory, EditCategory)

urlpatterns = [
    # categories
    path("", login_required(Categories.as_view()),
         name="categories"),
    path("categories/<int:pk>/", login_required(CategoriesChildren.as_view()),
         name="categories_children"),
    path("categories/add/", login_required(AddCategory.as_view()),
         name="add_category"),
    path("categories/edit/<int:pk>/", login_required(EditCategory.as_view()),
         name="edit_category"),
    path("categories/delete/<int:pk>/",
         login_required(DeleteCategory.as_view()), name="delete_category"),
]
