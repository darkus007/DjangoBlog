from django.views.generic import ListView, DetailView

from blog.models import Post


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = 'time_created'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
