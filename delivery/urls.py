from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (DeliveryNotes, AddNote)

urlpatterns = [
    path("", login_required(DeliveryNotes.as_view()),
         name="delivery_notes"),
    path("delivery/add/", login_required(AddNote.as_view()),
         name="delivery_add_note"),
]
