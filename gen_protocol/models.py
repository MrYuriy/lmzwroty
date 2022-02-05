from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField, TextField
import datetime
from django.utils import timezone
class Product(models.Model):
    sku = models.IntegerField()
    name = models.CharField(max_length=26)
    quantity = models.IntegerField()
    quantity_not_damaget = models.IntegerField()
    quantity_damage = models.IntegerField()
    
    def __str__(self):
        return self.name

class Order(models.Model):
    palete = "P"
    box = "C"
    date_writes = models.DateField()
    TAPE_OF_DELIVERY_CHOICES = {
            (palete, "P"),
            (box, "C")
        }

    nr_order = models.IntegerField()
    tape_of_delivery = models.CharField(
            max_length=1,
            choices=TAPE_OF_DELIVERY_CHOICES,
            default=box
        )
    def __str__(self):
        return 'Order {}'.format(str(self.nr_order))
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # class Meta:
    #     unique_together = ('order', 'product')

class SkuName(models.Model):
    sku = IntegerField()
    name_of_produckt = CharField(max_length=100)

    def __str__(self):
        return self.name_of_produckt