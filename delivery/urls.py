from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (DeliveryNotes, AddNote, EditNote, DeleteNote, AddCustomer)

urlpatterns = [
    path("", login_required(DeliveryNotes.as_view()),
         name="delivery_notes"),
    path("add/customer/", login_required(AddCustomer.as_view()),
         name="delivery_add_customer"),
    path("add/", login_required(AddNote.as_view()),
         name="delivery_add_note"),
    path("edit/<int:pk>/", login_required(EditNote.as_view()),
         name="delivery_edit_note"),
    path("delete/<int:pk>/", login_required(DeleteNote.as_view()),
         name="delivery_delete_note"),
]
