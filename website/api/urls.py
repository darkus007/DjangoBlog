from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import api_category, APIPostView, APIPostDetailView  # APIPostViewSet

# router = DefaultRouter()
# router.register('posts', APIPostViewSet)

urlpatterns = [
    path('categories/', api_category, name='api-category'),
    # path('', include(router.urls)),
    path('posts/<slug:slug>/', APIPostDetailView.as_view(), name='api-post-detail'),
    path('posts/', APIPostView.as_view(), name='api-post'),
]
