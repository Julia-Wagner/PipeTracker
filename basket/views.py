from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django_tables2 import RequestConfig
from django.contrib import messages

from .models import Basket, BasketItem
from .tables import BasketTable
from delivery.models import Note


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

        # create basket items dictionary
        items_dic = []
        for row in table.rows:
            item_dic = {}
            for column, cell in row.items():
                # use verbose name for heading
                item_dic[column.verbose_name] = cell
            items_dic.append(item_dic)

        # get available delivery notes
        notes = Note.objects.filter(status="open").all()

        context["notes"] = notes
        context["table"] = table
        context["items_dic"] = items_dic
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

        # decrease basket item quantity
        basket_item.quantity -= 1
        basket_item.save()

        # increase stock item quantity
        stock_item.quantity += 1
        stock_item.save()

        messages.success(request,
                         f"{stock_item} quantity changed.")

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
