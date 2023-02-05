from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets

from blog.models import Category, Post
from .serializers import CategorySerializer, PostSerializer
from website.utilites import slugify


@api_view(['GET', 'POST'])      # декоратор только задействует web-представление, работает и без него
@permission_classes((IsAuthenticatedOrReadOnly, ))  # isAdminUser - только админ или персонал
def api_category(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        # return JsonResponse(serializer.data, safe=False)      # без декоратора @api_view(['GET'])
        return Response(serializer.data)                        # с декоратором @api_view(['GET'])
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'info': 'Только администраторы сайта могут добавлять статьи.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Неправильный запрос.'}, status=status.HTTP_400_BAD_REQUEST)


# class APIPost(generics.ListCreateAPIView):    # только GET и POST
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )

#     def perform_create(self, serializer):
#         """ Добавляем пользователя и slug """
#         serializer.save(user=self.request.user)
#         serializer.save(slug=slugify(self.request.POST.get('title')))

class APIPostViewSet(viewsets.ModelViewSet):
    """ Метаконтроллер, выполняет все действия (выдача ресурсов, формирование адресов) """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    slug_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        """ Добавляем пользователя и slug """
        serializer.save(user=self.request.user)
        serializer.save(slug=slugify(self.request.POST.get('title')))


class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):     #
    queryset = Post.objects.all()
    serializer_class = PostSerializer
