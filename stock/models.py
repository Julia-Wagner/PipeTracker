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
