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
        return str(self.number)
