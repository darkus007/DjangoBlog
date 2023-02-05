from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import api_category, APIPostViewSet

router = DefaultRouter()
router.register('posts', APIPostViewSet)

urlpatterns = [
    path('categories/', api_category),
    path('', include(router.urls)),
    # path('posts/', APIPost.as_view()),
]