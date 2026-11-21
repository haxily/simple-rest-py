from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)]
    )

    def __str__(self):
        return self.name
