from django.utils import timezone
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    image = models.URLField(max_length=500)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Интсрумент'
        verbose_name_plural = 'Инструменты'
