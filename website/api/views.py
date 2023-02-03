from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Category
from .serializers import CategorySerializer


@api_view(['GET'])      # декоратор только задействует web-представление, работает и без него
def api_category(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        # return JsonResponse(serializer.data, safe=False)      # без декоратора @api_view(['GET'])
        return Response(serializer.data)                        # с декоратором @api_view(['GET'])
