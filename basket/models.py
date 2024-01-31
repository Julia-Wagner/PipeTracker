from django.db import models
from django.contrib.auth.models import User
from stock.models import Item


class Basket(models.Model):
    """
    Model to manage baskets.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through="BasketItem")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Basket for {self.user.username}"


class BasketItem(models.Model):
    """
    Model to manage basket items.
    """
    basket = models.ForeignKey(Basket, related_name="basket_items",
                               on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ["item__matchcode"]

    def __str__(self):
        return f"{self.basket} - {self.item} ({self.quantity})"
