# views.py (Order creation view)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Customer
from .serializers import CustomerSerializer
from .serializers import OrderSerializer

class CreateOrderView(APIView):
    def post(self, request):
        customer_instance = None

        if request.user.is_authenticated:
            customer_instance = getattr(request.user, 'customer', None)

        else:
            customer_data = request.data.get("customer", None)
            if customer_data:
                serializer = CustomerSerializer(data=customer_data)
                if serializer.is_valid():
                    customer_instance = serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            customer = customer_instance,
            items = request.data.get("items", []),
            price = request.data.get("price", 0.0)
        )

        return Response({
            "order_id": order.id,
            "status": "success",
            "customer":CustomerSerializer(customer_instance).data if customer_instance else None
        }, status=status.HTTP_201_BAD_REQUEST)




class CustomerListCreateView(APIView):
    def get(self, request):
        # Fetch and return all customers ordered by created_at descending
        customers = Customer.objects.all().order_by('-created_at')
        serializers = CustomerSerializer(customers, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Validate and create a new customer
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






class CustomerOrderListView(APIView):
    def get(self, request):
        orders = None

        # Case-1: Authenticated user
        if request.user.is_authenticated:
            customer = getattr(request.user, "customer", None)
            if not customer:
                return Response({"detail": "No customer profile linked to user."},
                                status=status.HTTP_404_NOT_FOUND)
            orders = Order.objects.filter(customer=customer)

        # Case-2: query param customer_id
        else:
            customer_id = request.query_param.get("customer_id")
            if not customer_id:
                return Response({
                    "detail": "customer id is required for customer lookup."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                customer = Customer.objects.get(pk=customer_id)
                orders = Order.object.filter(customer=customer)
            except Customer.DoesNotExist:
                return Response({"detail": "Customer not found."},
                                status=status.HTTP_404_NOT_FOUND)
        
        # Serializer orders (latest first)
        serializer = OrderSerializer(orders.order_by("-created_at"), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    








class CreateOrderView(APIView):
    def post(self, request):
        customer_instance = None

        if request.user.is_authenticated:
            customer_instance = getattr(request.user, 'customer', None)

        else:
            customer_data = request.data.get("customer", None)
            if customer_data:
                serializer = CustomerSerializer(data=customer_data)
                if serializer.is_valid():
                    customer_instance = serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            customer = customer_instance,
            items = request.data.get("items", []),
            price = request.data.get("price", 0.0)
        )

        return Response({
            "order_id": order.id,
            "status": "success",
            "customer":CustomerSerializer(customer_instance).data if customer_instance else None
        }, status=status.HTTP_201_CREATED)