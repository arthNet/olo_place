from django.db import models

# Create your models here.

class Ogloszenia(models.Model):
    # potrzebne wszyskie dane ogloszenia

    title = models.CharField(max_length=512)
    description = models.CharField(max_length=512)
    price = models.IntegerField()

    def __str__(self):
        return (f"Id: {id.self}")