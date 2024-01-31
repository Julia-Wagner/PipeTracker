from django.db import models
from django.contrib.auth.models import User

from stock.models import Item


class Customer(models.Model):
    """
    Model to manage customers.
    """
    user = models.ForeignKey(User, related_name="created_customers",
                             on_delete=models.CASCADE)
    number = models.IntegerField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.number})"


class Note(models.Model):
    """
    Model to manage delivery notes.
    """
    user = models.ForeignKey(User, related_name="created_notes",
                             on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="assigned_notes",
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    status = models.CharField(max_length=100,
                              choices=[("open", "Open"), ("closed", "Closed")],
                              default="open")
    date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, through="NoteItem")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        customer_str = f"{self.customer.first_name} {self.customer.last_name}"
        return f"{self.title} ({customer_str})"

    def basket_text(self):
        """
        Format the text to show in basket select field.
        :return:
        """
        date = self.date.strftime('%d.%m.%Y')
        return (f"{self.title} for {self.customer.first_name} "
                f"{self.customer.last_name} ({date})")

    def get_total(self):
        """
        Calculate the total for all stock items in the delivery note.
        :return: calculated total
        """
        note_items = NoteItem.objects.filter(note=self)
        # https://stackoverflow.com/questions/68960662/django-sum-values-of-from-a-for-loop-in-template
        return sum([(delivery_item.item.price * delivery_item.quantity)
                    for delivery_item in note_items])


class NoteItem(models.Model):
    """
    Model to manage delivery note items.
    """
    note = models.ForeignKey(Note, related_name="note_items",
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ["item__matchcode"]

    def __str__(self):
        return f"{self.note} - {self.item} ({self.quantity})"
