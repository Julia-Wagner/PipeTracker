from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, ListView, UpdateView,
                                  DeleteView, DetailView)
from django_tables2 import RequestConfig
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph, KeepTogether,
                                Table, TableStyle)
import io

from .models import Note, Customer, NoteItem
from .forms import NoteForm, CustomerForm
from .tables import NoteTable, NoteDetailsTable


class DeliveryNotes(ListView):
    """
    List all delivery notes.
    """
    template_name = "delivery/delivery_notes.html"
    model = Note
    context_object_name = "notes"

    def get_context_data(self, **kwargs):
        """
        Add the table with delivery notes to the context for the template.
        :param kwargs:
        :return: the context
        """
        context = super().get_context_data(**kwargs)

        notes = Note.objects.all()

        # create and configure stock items table
        table = NoteTable(notes)
        RequestConfig(self.request).configure(table)

        context["table"] = table

        return context


class AddCustomer(CreateView):
    """
    Add customers view.
    """
    template_name = "delivery/add_customer.html"
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy("delivery_add_note")

    def form_valid(self, form):
        """
        Validate the form.
        :param form:
        :return: success message and response
        """
        form.instance.user = self.request.user
        response = super(AddCustomer, self).form_valid(form)
        # add success message
        messages.success(self.request,
                         "Customer created successfully.")
        return response


class AddNote(CreateView):
    """
    Add delivery notes view.
    """
    template_name = "delivery/add_note.html"
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("delivery_notes")

    def form_valid(self, form):
        """
        Validate the form.
        :param form:
        :return: success message and response
        """
        form.instance.user = self.request.user
        response = super(AddNote, self).form_valid(form)
        # add success message
        messages.success(self.request,
                         "Delivery note created successfully.")
        return response


class EditNote(UpdateView):
    """
    Edit a delivery note.
    """
    template_name = "delivery/edit_note.html"
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("delivery_notes")

    def dispatch(self, request, *args, **kwargs):
        """
        Don´t allow editing for closed notes, only for superusers.
        :param request:
        :param args:
        :param kwargs:
        :return: redirect or parent dispatch method
        """
        note = self.get_object()

        if note.status == "closed":
            if not request.user.is_superuser:
                (messages.error
                 (request, "Closed delivery notes can not be edited."))
                return redirect("/delivery/")

        # call parent dispatch method
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Validate the form.
        :param form:
        :return: success message and response
        """
        response = super().form_valid(form)
        messages.success(self.request, "Changes saved.")
        return response


class DeleteNote(DeleteView):
    """
    Delete a delivery note.
    """
    model = Note
    success_url = reverse_lazy("delivery_notes")

    def dispatch(self, request, *args, **kwargs):
        """
        Don´t allow deleting for closed notes, only for superusers.
        :param request:
        :param args:
        :param kwargs:
        :return: redirect or parent dispatch method
        """
        note = self.get_object()

        if note.status == "closed":
            if not request.user.is_superuser:
                (messages.error
                 (request, "Closed delivery notes can not be deleted."))
                return redirect("/delivery/")

        # call parent dispatch method
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Validate the form.
        :param form:
        :return: success message and response
        """
        response = super().form_valid(form)
        messages.success(self.request, "Delivery note deleted.")
        return response


class NoteDetail(DetailView):
    """
    Detail view for a delivery note.
    """
    template_name = "delivery/note_detail.html"
    model = Note
    context_object_name = "note"

    def get_context_data(self, **kwargs):
        """
        Add the table with stock items and the total cost for the note
        to the context for the template.
        :param kwargs:
        :return: the context
        """
        context = super().get_context_data(**kwargs)

        note_items = NoteItem.objects.filter(note=self.object)

        # create and configure note items table
        table = NoteDetailsTable(note_items)
        RequestConfig(self.request).configure(table)

        total_cost = self.object.get_total()

        context["table"] = table
        context["total_cost"] = total_cost

        return context


class DeliveryItemDecrease(View):
    """
    Decrease the quantity of the delivery item.
    """
    def get(self, request, *args, **kwargs):
        """
        Check the available quantity, decrease the note item quantity
        and increase the stock item quantity.
        :param request:
        :param args:
        :param kwargs:
        :return: a success/error message and redirect to the delivery note
        """
        delivery_item_id = self.kwargs.get("pk")
        delivery_item = get_object_or_404(NoteItem, id=delivery_item_id)
        stock_item = delivery_item.item

        # don´t allow changing the quantity for a closed delivery note
        if delivery_item.note.status == "closed":
            (messages.error
             (request, "Closed delivery notes can not be edited."))
            return redirect("delivery_note_detail", pk=delivery_item.note.id)

        # check if the item should remain in the delivery note after decreasing
        if delivery_item.quantity > 1:
            # decrease delivery item quantity
            delivery_item.quantity -= 1
            delivery_item.save()

            # increase stock item quantity
            stock_item.quantity += 1
            stock_item.save()

            messages.success(request,
                             f"{stock_item} quantity changed.")
        # remove the item from the delivery note
        elif delivery_item.quantity == 1:
            # decrease delivery item quantity
            delivery_item.delete()

            # increase stock item quantity
            stock_item.quantity += 1
            stock_item.save()

            messages.success(request,
                             f"{stock_item} removed from delivery note.")
        else:
            messages.error(request,
                           "Quantity can not be less than 0.")

        return redirect("delivery_note_detail", pk=delivery_item.note.id)


class DeliveryItemIncrease(View):
    """
    Increase the quantity of the delivery item.
    """
    def get(self, request, *args, **kwargs):
        """
        Check the available quantity, increase the note item quantity
        and decrease the stock item quantity.
        :param request:
        :param args:
        :param kwargs:
        :return: a success/error message and redirect to the delivery note
        """
        delivery_item_id = self.kwargs.get("pk")
        delivery_item = get_object_or_404(NoteItem, id=delivery_item_id)
        stock_item = delivery_item.item

        # don´t allow changing the quantity for a closed delivery note
        if delivery_item.note.status == "closed":
            (messages.error
             (request, "Closed delivery notes can not be edited."))
            return redirect("delivery_note_detail", pk=delivery_item.note.id)

        # check if there are stock items available
        if stock_item.quantity >= 1:
            # increase delivery item quantity
            delivery_item.quantity += 1
            delivery_item.save()

            # decrease stock item quantity
            stock_item.quantity -= 1
            stock_item.save()

            messages.success(request,
                             f"{stock_item} quantity changed.")
        else:
            messages.error(request,
                           f"No more {stock_item} available.")

        return redirect("delivery_note_detail", pk=delivery_item.note.id)


class ExportPDF(View):
    """
    Export the details of a delivery note to a PDF file.
    """
    def get(self, request, *args, **kwargs):
        """
        Create and download a PDF file from the delivery note.
        :param request:
        :param args:
        :param kwargs:
        :return: file response
        """
        note = Note.objects.get(pk=self.kwargs["pk"])
        note_items = NoteItem.objects.filter(note=note)

        # create a file-like buffer for the PDF
        buffer = io.BytesIO()

        # create the PDF object
        pdf = SimpleDocTemplate(buffer, pagesize=A4)

        # add PDF content
        content = []

        # add title, customer, date, and total value as a paragraph
        # load styles and customize headings
        styles = getSampleStyleSheet()
        heading1 = styles["Heading1"]
        heading1.spaceAfter = 10
        heading1.textColor = (0.15234375, 0.25, 0.375)
        heading2 = styles["Heading2"]
        heading2.spaceAfter = 20
        heading2.textColor = (0.73046875, 0.08203125, 0.08203125)

        note_paragraph = Paragraph(f"Delivery Note: {note.title}",
                                   heading1)
        customer_paragraph = Paragraph(f"For: {note.customer}",
                                       styles["Heading3"])
        date_paragraph = Paragraph(f"Created: "
                                   f"{note.date.strftime('%d.%m.%Y')}",
                                   styles["Heading3"])
        total_paragraph = Paragraph(f"Total value: € {note.get_total()}",
                                    heading2)
        content.append(KeepTogether([note_paragraph]))
        content.append(KeepTogether([customer_paragraph]))
        content.append(KeepTogether([date_paragraph]))
        content.append(KeepTogether([total_paragraph]))

        # generate table
        table = self.generate_table_content(note_items)

        # add the table to the content
        content.append(table)

        # build PDF
        pdf.build(content)

        # file response with PDF content
        buffer.seek(0)
        file_name = f"{note.title}_{note.customer.last_name}.pdf"
        response = FileResponse(buffer, as_attachment=True,
                                filename=file_name)
        return response

    def generate_table_content(self, note_items):
        """
        Generate the table content and apply styling.
        :param note_items:
        :return: generated table
        """
        # add table headers
        table_data = [
            ["Quantity", "Name", "Size", "Matchcode", "Total Price"]
        ]

        # add table content for each delivery item
        for note_item in note_items:
            table_data.append([
                note_item.quantity,
                note_item.item.name,
                note_item.item.size,
                note_item.item.matchcode,
                f"€ {note_item.item.price * note_item.quantity}"
            ])

        # create the table element
        table = Table(table_data)

        # customize style
        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.Color(0.15234375, 0.25, 0.375)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
        ])

        # apply style
        table.setStyle(style)

        return table
