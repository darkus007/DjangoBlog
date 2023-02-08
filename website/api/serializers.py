from rest_framework import serializers
from blog.models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # скрываем поля пользователя и slug
    # они будут добавлены в классе представления через функцию perform_create
    user = serializers.ReadOnlyField(source='user.username')
    slug = serializers.ReadOnlyField()
    likes = serializers.PrimaryKeyRelatedField(many=True, allow_empty=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'cat', 'title', 'slug', 'body', 'time_created', 'likes')
        # depth = 1
