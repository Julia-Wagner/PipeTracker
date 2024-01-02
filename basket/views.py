from django.views.generic import ListView
from django_tables2 import RequestConfig
from .models import Basket, BasketItem


class BasketItems(ListView):
    """
    List all basket items
    """
    template_name = "basket/basket_list.html"
    model = Basket

    def get_queryset(self):
        # get basket for logged-in user
        return Basket.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        basket = self.get_queryset().first()
        basket_items = BasketItem.objects.filter(basket=basket)

        context["basket_items"] = basket_items

        return context

