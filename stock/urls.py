from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (AddCategory, Categories, CategoriesChildren,
                    DeleteCategory, EditCategory,
                    Items, AddItem, EditItem, DeleteItem, ItemToBasket,
                    StockItemDecrease, StockItemIncrease)

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
    path("items/add/", login_required(AddItem.as_view()),
         name="stock_add_item"),
    path("items/edit/<int:pk>/", login_required(EditItem.as_view()),
         name="stock_edit_item"),
    path("items/delete/<int:pk>/",
         login_required(DeleteItem.as_view()),
         name="stock_delete_item"),
    # add stock items to the basket
    path("basket/<int:pk>/",
         login_required(ItemToBasket.as_view()),
         name="stock_to_basket"),
    # decrease increase stock item quantity
    path("quantity/decrease/<int:pk>/",
         login_required(StockItemDecrease.as_view()),
         name="stock_quantity_decrease"),
    path("quantity/increase/<int:pk>/",
         login_required(StockItemIncrease.as_view()),
         name="stock_quantity_increase"),
]
