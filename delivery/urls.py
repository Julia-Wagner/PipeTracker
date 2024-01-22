from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (DeliveryNotes, AddNote, EditNote, DeleteNote, AddCustomer,
                    NoteDetail, DeliveryItemDecrease, DeliveryItemIncrease,
                    ExportPDF)

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
    path("<int:pk>/", login_required(NoteDetail.as_view()),
         name="delivery_note_detail"),

    # decrease increase delivery item quantity
    path("quantity/decrease/<int:pk>/",
         login_required(DeliveryItemDecrease.as_view()),
         name="delivery_quantity_decrease"),
    path("quantity/increase/<int:pk>/",
         login_required(DeliveryItemIncrease.as_view()),
         name="delivery_quantity_increase"),

    # export as PDF
    path("<int:pk>/export/",
         login_required(ExportPDF.as_view()),
         name="delivery_export_note"),

]
