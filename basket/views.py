from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django_tables2 import RequestConfig
from django.contrib import messages

from .models import Basket, BasketItem
from .tables import BasketTable
from delivery.models import Note, NoteItem


class BasketItems(ListView):
    """
    List all basket items
    """
    template_name = "basket/basket_items.html"
    model = Basket

    def get_queryset(self):
        # get basket for logged-in user
        return Basket.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        basket = self.get_queryset().first()
        basket_items = BasketItem.objects.filter(basket=basket)

        # create and configure basket items table
        table = BasketTable(basket_items)
        RequestConfig(self.request).configure(table)

        # get available delivery notes
        notes = Note.objects.filter(status="open").all()

        context["basket"] = basket
        context["notes"] = notes
        context["table"] = table
        context["basket_items"] = basket_items

        return context


class BasketItemDecrease(View):
    """
    Decrease the quantity of the basket item
    """
    def get(self, request, *args, **kwargs):
        basket_item_id = self.kwargs.get("pk")
        basket_item = get_object_or_404(BasketItem, id=basket_item_id)
        stock_item = basket_item.item

        if basket_item.quantity > 1:
            # decrease basket item quantity
            basket_item.quantity -= 1
            basket_item.save()

            # increase stock item quantity
            stock_item.quantity += 1
            stock_item.save()

            messages.success(request,
                             f"{stock_item} quantity changed.")
        elif basket_item.quantity == 1:
            # decrease basket item quantity
            basket_item.delete()

            # increase stock item quantity
            stock_item.quantity += 1
            stock_item.save()

            messages.success(request,
                             f"{stock_item} removed from basket.")
        else:
            messages.error(request,
                           f"Quantity can not be less than 0.")

        return redirect("/basket/")


class BasketItemIncrease(View):
    """
    Increase the quantity of the basket item
    """
    def get(self, request, *args, **kwargs):
        basket_item_id = self.kwargs.get("pk")
        basket_item = get_object_or_404(BasketItem, id=basket_item_id)
        stock_item = basket_item.item

        if stock_item.quantity >= 1:
            # increase basket item quantity
            basket_item.quantity += 1
            basket_item.save()

            # decrease stock item quantity
            stock_item.quantity -= 1
            stock_item.save()

            messages.success(request,
                             f"{stock_item} quantity changed.")
        else:
            messages.error(request,
                           f"No more {stock_item} available.")

        return redirect("/basket/")


class BasketToNote(View):
    """
    Add the items of the basket to the selected delivery note
    """
    def post(self, request, *args, **kwargs):
        note_param = request.POST.get("note")
        note_id = int(note_param)
        basket_id = self.kwargs.get("pk")
        basket = get_object_or_404(Basket, id=basket_id)
        basket_items = basket.basket_items.all()
        note = get_object_or_404(Note, id=note_id)

        for basket_item in basket_items:
            stock_item = basket_item.item
            # check if item is already in delivery note
            exists = NoteItem.objects.filter(note=note,
                                             item=stock_item).exists()

            # update item if already in delivery note
            if exists:
                note_item = NoteItem.objects.get(note=note, item=stock_item)
                note_item.quantity += basket_item.quantity
                note_item.save()
            # create new item
            else:
                NoteItem.objects.create(note=note, item=stock_item,
                                        quantity=basket_item.quantity),

            # remove item from basket
            basket_item.delete()

        messages.success(request,
                         f"Stock items added to your delivery note.")

        return redirect("delivery_note_detail", pk=note_id)
