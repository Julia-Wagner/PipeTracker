from django.views.generic import ListView
from django_tables2 import RequestConfig
from .models import Basket, BasketItem
from .tables import BasketTable


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

        context["table"] = table
        context["items_dic"] = items_dic
        context["basket_items"] = basket_items

        return context

