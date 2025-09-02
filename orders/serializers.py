# serializers.py
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "total_price", "status", "created_at"]  # sirf important fields
