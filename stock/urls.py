from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (AddCategory, Categories, CategoriesChildren,
                    DeleteCategory, EditCategory, Items)

urlpatterns = [
    # categories
    path("", login_required(Categories.as_view()),
         name="stock_categories"),
    path("categories/<int:pk>/", login_required(CategoriesChildren.as_view()),
         name="stock_categories_children"),
    path("categories/add/", login_required(AddCategory.as_view()),
         name="stock_add_category"),
    path("categories/edit/<int:pk>/", login_required(EditCategory.as_view()),
         name="stock_edit_category"),
    path("categories/delete/<int:pk>/",
         login_required(DeleteCategory.as_view()),
         name="stock_delete_category"),
    # stock items
    path("categories/<int:pk>/items/", login_required(Items.as_view()),
         name="stock_items"),
]
