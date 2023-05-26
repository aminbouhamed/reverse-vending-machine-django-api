from django.db import models
from account.models import Account

class RecyclableItem(models.Model):
    CONTAINER_CHOICES = (
        ('BOTTLE', 'Bottle'),
        ('CAN', 'Can')
    )
    MATERIAL_CHOICES = (
        ('PLASTIC', 'Plastic'),
        ('ALUMINIUM', 'Aluminium')
    )
    BEVERAGE_TYPE_CHOICES = (
        ('WATER', 'Water'),
        ('SODA', 'Soda')
    )

    container = models.CharField(max_length=30, choices=CONTAINER_CHOICES)
    material = models.CharField(max_length=30, choices=MATERIAL_CHOICES)
    brand = models.CharField(max_length=30)
    volume = models.FloatField()
    beverageType = models.CharField(max_length=30, choices=BEVERAGE_TYPE_CHOICES)    


class RVM(models.Model):
    class Status(models.IntegerChoices):
        FAULTY = 0
        WORKING = 1
        MAINTENANCE = 2
    address = models.CharField(max_length=200)
    status = models.IntegerField(choices=Status.choices)

class RecyclingTransaction(models.Model):
    client = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    transactionDate = models.DateTimeField()
    totalRecompense = models.FloatField()
    rvm = models.ForeignKey(RVM, on_delete=models.CASCADE)

class RecyclingHistory(models.Model):
    class Meta:
        unique_together = (('recyclingTransaction', 'recyclableItem'))

    recyclingTransaction = models.ForeignKey(RecyclingTransaction, on_delete=models.CASCADE)
    recyclableItem = models.ForeignKey(RecyclableItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()