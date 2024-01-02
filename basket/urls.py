from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (BasketItems)

urlpatterns = [
    path("", login_required(BasketItems.as_view()),
         name="basket_items"),
]
