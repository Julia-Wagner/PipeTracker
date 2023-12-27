from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (DeliveryNotes)

urlpatterns = [
    path("", login_required(DeliveryNotes.as_view()),
         name="delivery_notes"),
]
