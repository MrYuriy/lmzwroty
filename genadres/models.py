from django.db import models

# Create your models here.
class Adres(models.Model):
    adreses = models.TextField(blank=True)

class User(models.Model):
    name = models.CharField(max_length = 25)
    from_location = models.CharField(max_length = 2)
    to_location = models.CharField(max_length = 2)

    inventory_adres = models.CharField(max_length = 2)
    inventory_qty = models.CharField(max_length = 2)

    from_location_arc = models.CharField(max_length = 2)
    to_location_arc = models.CharField(max_length = 2)


    def __str__(self):
        return self.name