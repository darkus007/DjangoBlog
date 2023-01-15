from django.urls import path

from blog.views import HomeView, PostDetailView, AddPostView, UpdatePostView, DeletePostView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('add-post/', AddPostView.as_view(), name='post-add'),
    path('update-post/<slug:slug>/', UpdatePostView.as_view(), name='post-update'),
    path('delete-post/<slug:slug>/', DeletePostView.as_view(), name='post-delete'),
]
