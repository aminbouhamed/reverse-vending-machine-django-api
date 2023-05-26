from rest_framework import serializers
from .models import *

class RecyclableItemSerializer(serializers.ModelSerializer):
    container = serializers.ChoiceField(choices=RecyclableItem.CONTAINER_CHOICES)
    material = serializers.ChoiceField(choices=RecyclableItem.MATERIAL_CHOICES)
    brand = serializers.CharField(max_length=30)
    volume = serializers.FloatField()
    beverageType = serializers.ChoiceField(choices=RecyclableItem.BEVERAGE_TYPE_CHOICES)
    class Meta:
        model = RecyclableItem
        fields = '__all__'

class RVMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RVM
        fields = '__all__'

class RecyclingTransactionSerializer(serializers.ModelSerializer):
    rvm_address = serializers.CharField(source='rvm.address', read_only=True)
    class Meta:
        model = RecyclingTransaction
        fields = ['id', 'transactionDate', 'rvm_address', 'totalRecompense']

class RecyclingHistorySerializer(serializers.ModelSerializer):
    item_container = serializers.CharField(source='recyclableItem.container', read_only=True)
    item_brand = serializers.CharField(source='recyclableItem.brand', read_only=True)
    item_volume = serializers.CharField(source='recyclableItem.volume', read_only=True)
    class Meta:
        model = RecyclingHistory
        fields = ['item_container', 'item_brand', 'item_volume', 'quantity']
