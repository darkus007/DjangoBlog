from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views

from blog.models import Category, Post
from .serializers import CategorySerializer, PostSerializer
from website.utilites import slugify


@api_view(['GET', 'POST'])      # декоратор только задействует web-представление, работает и без него
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_category(request) -> Response:
    """
    Функция представления для Категорий.
    Читать могут все, добавлять только персонал сайта.
    """
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        # return JsonResponse(serializer.data, safe=False)      # без декоратора @api_view(['GET'])
        return Response(serializer.data)                        # с декоратором @api_view(['GET'])
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(slug=slugify(serializer.validated_data['title']))
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'info': 'Только администраторы сайта могут добавлять статьи.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Неправильный запрос.'}, status=status.HTTP_400_BAD_REQUEST)


class APIPostView(views.APIView):
    """
    Класс представления для работы со статьями (Постами).
    Реализованы методы GET - возвращает все статьи и
    POST - добавляет статью.
    """

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request) -> Response:
        posts = Post.objects.select_related('user', 'cat').prefetch_related('likes').order_by('-time_created', 'cat')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request) -> Response:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            serializer.save(slug=slugify(serializer.validated_data['title']))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIPostDetailView(views.APIView):
    """
    Класс представления для работы со статьей (Постом).
    Реализованы методы: GET (возвращает статью), PUT, PATCH и DELETE.
    """

    def get(self, request, slug) -> Response:
        post = Post.objects.select_related('user', 'cat').prefetch_related('likes').get(slug=slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, slug) -> Response:
        return self.put_patch(request=request, slug=slug)

    def patch(self, request, slug):
        return self.put_patch(request=request, slug=slug)

    def delete(self, request, slug) -> Response:
        post = Post.objects.get(slug=slug)
        if post.user == request.user or request.user.is_staff:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'info': 'Удалить статью может только ее автор.'})

    @staticmethod
    def put_patch(request, slug) -> Response:
        """
        Обновляет статью. Используется в методах PUT и PATCH.
        Правка статьи доступна только ее автору или персоналу сайта.
        """
        post = Post.objects.get(slug=slug)
        if post.user == request.user or request.user.is_staff:
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'info': 'Обновить статью может только ее автор.'})
