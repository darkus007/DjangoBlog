from django.urls import path, include

from .views import api_category, APIPostView, APIPostDetailView

urlpatterns = [
    path('categories/', api_category, name='api-category'),
    path('posts/<slug:slug>/', APIPostDetailView.as_view(), name='api-post-detail'),
    path('posts/', APIPostView.as_view(), name='api-post'),
]
