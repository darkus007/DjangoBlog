from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Category
from .forms import PostForm, CategoryForm


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ('-time_created', )
    paginate_by = 50


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class AddPostView(CreateView):
    model = Post
    form_class = PostForm  # подключаем стилизованную форму
    template_name = 'blog/post_add.html'
    # fields = '__all__'  # какие поля отображать (уже описаны в PostForm)
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """ Передаем пользователя в форму """
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'
    success_url = reverse_lazy('home')


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')


class CategoryView(ListView):
    model = Category
    template_name = 'blog/category_all.html'
    ordering = ('title', )


class AddCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_add.html'
    success_url = reverse_lazy('categories')


class UpdateCategoryView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_update.html'
    success_url = reverse_lazy('categories')


class DeleteCategoryView(DeleteView):
    model = Category
    template_name = 'blog/category_delete.html'
    success_url = reverse_lazy('categories')
