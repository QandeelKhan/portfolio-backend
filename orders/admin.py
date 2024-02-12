from django.contrib import admin
from .models import Order, OrderProgress


class OrderProgressInline(admin.StackedInline):
    model = OrderProgress
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'user', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'order_type')
    search_fields = ('project_name', 'user__username')
    inlines = (OrderProgressInline,)


@admin.register(OrderProgress)
class OrderProgressAdmin(admin.ModelAdmin):
    list_display = ('order', 'frontend_percentage',
                    'backend_percentage', 'design_percentage')
    list_filter = ('order',)
    search_fields = ('order__project_name', 'order__user__username')
