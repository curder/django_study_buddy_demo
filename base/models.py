from django.db import models


class Room(models.Model):
    # host =
    # topic =
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    # participants =
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
