from rest_framework import generics
from .models import Order, OrderProgress
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import OrderSerializer, OrderProgressSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:  # show all orders for staff and superusers
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderProgressListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderProgress.objects.all()
    serializer_class = OrderProgressSerializer


class OrderProgressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderProgress.objects.all()
    serializer_class = OrderProgressSerializer
