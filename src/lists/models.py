from django.urls import reverse
from django.db import models
from django.conf import settings


class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lists",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(
        List,
        default=None,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("id",)
        unique_together = ("text", "list")

    def __str__(self):
        return self.text
