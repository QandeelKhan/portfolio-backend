from django.urls import path
from .views import (
    OrderListCreateAPIView,
    OrderDetailAPIView,
    OrderProgressListCreateAPIView,
    OrderProgressDetailAPIView,
)

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('order-progress/', OrderProgressListCreateAPIView.as_view(),
         name='order_progress_list_create'),
    path('order-progress/<int:pk>/', OrderProgressDetailAPIView.as_view(),
         name='order_progress_detail'),
]
