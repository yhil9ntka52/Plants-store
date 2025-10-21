from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Plant, Category, User, Cart, Order, OrderItem
from .serializers import PlantSerializer, CategorySerializer, UserSerializer, CartSerializer, OrderSerializer

class CartList(APIView):
    def get(self, request):
        carts = Cart.objects.filter(user_id=request.user.id)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDelete(APIView):
    def delete(self, request, item_id):
        try:
            item = Cart.objects.get(id=item_id, user_id=request.user.id)
        except Cart.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)
        item.delete()
        return Response(status=204)

class CartCheckout(APIView):
    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=400)
        order = Order.objects.create(user=user, status='created')
        for item in cart_items:
            OrderItem.objects.create(order=order, plant=item.plant, quantity=item.quantity)
        cart_items.delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderList(APIView):
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetail(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user_id=request.user.id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class PlantList(APIView):
    def get(self, request):
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlantDetail(APIView):
    def get(self, request, pk):
        try:
            plant = Plant.objects.get(pk=pk)
        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=404)
        serializer = PlantSerializer(plant)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            plant = Plant.objects.get(pk=pk)
        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=404)
        serializer = PlantSerializer(plant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            plant = Plant.objects.get(pk=pk)
        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=404)
        plant.delete()
        return Response(status=204)

class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        if category.plant_set.exists():
            return Response({'error': 'Cannot delete category while plants exist'}, status=400)
        category.delete()
        return Response(status=204)
