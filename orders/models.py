from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('in_progress', 'in_Progress'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    )

    PAYMENT_CHOICES = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('cancelled', 'cancelled')
    )

    TYPE_CHOICES = (
        ('e-commerce', 'e-commerce'),
        ('blog', 'blog'),
        ('custom', 'custom')
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='pending', null=True, blank=True)
    active_status = models.BooleanField(default=False, null=True, blank=True)
    payment_status = models.CharField(
        max_length=50, choices=PAYMENT_CHOICES, default='pending')
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name


class OrderProgress(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='progress')
    frontend_percentage = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True)
    backend_percentage = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True)
    design_percentage = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.project_name} Progress"
