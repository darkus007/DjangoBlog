from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .forms import AddPostForm


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ('-time_created', )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class AddPostView(CreateView):
    model = Post
    form_class = AddPostForm  # подключаем стилизованную форму
    template_name = 'blog/post_add.html'
    # fields = '__all__'  # какие поля отображать (уже описаны в AddPostForm)
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """ Передаем пользователя в форму """
        form.instance.user = self.request.user
        print(f'{form.instance.user=}')     # проверка
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = '__all__'
    success_url = reverse_lazy('home')


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')
