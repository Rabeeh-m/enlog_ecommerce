from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Q
from .models import Category, Product, UserProfile, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, UserProfileSerializer, OrderSerializer, RegisterSerializer
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        cache_key = 'categories_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)  # Cache for 1 hour
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def list(self, request):
        cache_key = 'products_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = self.get_queryset()
        # Apply filters
        category_id = request.query_params.get('category_id')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        in_stock = request.query_params.get('in_stock')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if in_stock:
            queryset = queryset.filter(stock__gt=0) if in_stock == 'true' else queryset.filter(stock=0)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            cache.set(cache_key, serializer.data, timeout=3600)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        items_data = request.data.get('items', [])
        if not items_data:
            return Response({"error": "No items provided"}, status=400)

        total_price = 0
        order = Order.objects.create(user=request.user, total_price=0)

        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'])
                quantity = item_data['quantity']
                if product.stock < quantity:
                    return Response({"error": f"Insufficient stock for product {product.name}"}, status=400)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                total_price += product.price * quantity
            except Product.DoesNotExist:
                return Response({"error": f"Product with id {item_data['product_id']} not found"}, status=404)

        order.total_price = total_price
        order.save()

        # Refresh order with related items for serialization
        order = Order.objects.prefetch_related('items__product').get(id=order.id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)