from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    Model to manage customers
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
    Model to manage delivery notes
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

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        customer_str = f"{self.customer.first_name} {self.customer.last_name}"
        return f"{self.title} ({customer_str})"
