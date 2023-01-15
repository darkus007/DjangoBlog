from django.urls import path

from blog.views import HomeView, PostDetailView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]
