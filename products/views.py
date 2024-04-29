from django.shortcuts import render
from products.models import Product
from products.serializers import ProductsSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache



@api_view(["GET"])
def product_list(request):
    cache_key = "product_list"

    if not cache.get(cache_key):
        print("cache miss")
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        json_data = serializer.data
        cache.set(cache_key, json_data, 5)

    response_data = cache.get(cache_key)
    return Response(response_data)

    
