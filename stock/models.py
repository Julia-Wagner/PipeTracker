from django.db import models
from django.contrib.auth.models import User

from django_resized import ResizedImageField


class Category(models.Model):
    """
    Model to manage categories
    """
    user = models.ForeignKey(User, related_name="created_categories",
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    image = ResizedImageField(
        size=[500, None], quality=75, upload_to="categories/",
        force_format="WEBP", null=False, blank=False
    )
    image_alt = models.CharField(max_length=100, null=False, blank=False)
    parent = models.ForeignKey("self", null=True, blank=True,
                               related_name="children",
                               on_delete=models.CASCADE)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return str(self.name)

    def get_parents(self):
        """
        Get all parents of the given category.
        :return: List of parents
        """
        parents = []
        current_parent = self.parent

        while current_parent is not None:
            parents.insert(0, current_parent)
            current_parent = current_parent.parent

        return parents


class Item(models.Model):
    """
    Model to manage stock items
    """
    user = models.ForeignKey(User, related_name="created_items",
                             on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=False, blank=False,
                                 related_name="stock_items",
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    matchcode = models.CharField(max_length=100, null=False, blank=False,
                                 unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=False,
                                blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    size = models.CharField(max_length=100, null=True, blank=True)
    details = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)
