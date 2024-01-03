from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (BasketItems, BasketItemDecrease, BasketItemIncrease)

urlpatterns = [
    path("", login_required(BasketItems.as_view()),
         name="basket_items"),
    path("quantity/decrease/<int:pk>/",
         login_required(BasketItemDecrease.as_view()),
         name="basket_quantity_decrease"),
    path("quantity/increase/<int:pk>/",
         login_required(BasketItemIncrease.as_view()),
         name="basket_quantity_increase"),
]
