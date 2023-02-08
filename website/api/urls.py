from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import api_category, APIPostView, APIPostDetailView  # APIPostViewSet

# router = DefaultRouter()
# router.register('posts', APIPostViewSet)

urlpatterns = [
    path('categories/', api_category),
    # path('', include(router.urls)),
    path('posts/<slug:slug>/', APIPostDetailView.as_view()),
    path('posts/', APIPostView.as_view()),
]
