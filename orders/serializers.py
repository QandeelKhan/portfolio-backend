from rest_framework import serializers
from .models import Order, OrderProgress


class OrderProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProgress
        fields = (
            'id',
            'order',
            'frontend_percentage',
            'backend_percentage',
            'design_percentage',
            'created_at',
            'updated_at'
        )


class OrderSerializer(serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'order_type',
            'status',
            'active_status',
            'payment_status',
            'project_name',
            'project_description',
            'total_price',
            'created_at',
            'due_date',
            'updated_at',
            'order_count'
        )

    def get_order_count(self, obj):
        return Order.objects.filter(user=obj.user).count()
