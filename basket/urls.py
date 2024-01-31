from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (BasketItems, BasketItemDecrease, BasketItemIncrease,
                    BasketToNote)

urlpatterns = [
    path("", login_required(BasketItems.as_view()),
         name="basket_items"),

    # decrease and increase the quantity of a basket item
    path("quantity/decrease/<int:pk>/",
         login_required(BasketItemDecrease.as_view()),
         name="basket_quantity_decrease"),
    path("quantity/increase/<int:pk>/",
         login_required(BasketItemIncrease.as_view()),
         name="basket_quantity_increase"),

    # add basket items to a delivery note
    path("<int:pk>/note/",
         login_required(BasketToNote.as_view()),
         name="basket_to_note"),
]
