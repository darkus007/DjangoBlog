from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from website.settings import ALL_CATEGORIES
from .models import Post, Category
from .forms import PostForm, CategoryForm


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ('-time_created',)
    paginate_by = 25

    def get_queryset(self):
        # return Post.objects.all().select_related('cat', 'user')
        return Post.objects.values('title', 'slug', 'body', 'time_created', 'user__username', 'cat__title', 'cat__slug')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = ALL_CATEGORIES.get('slug')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        # return Post.objects.filter(slug=self.kwargs['slug']).select_related('cat', 'user')
        return Post.objects.filter(slug=self.kwargs['slug']) \
            .values('title', 'slug', 'body', 'time_created', 'user__username', 'cat__title', 'user__id',
                    'user__first_name', 'user__last_name', 'user__profile__image', 'user__profile__website_url',
                    'user__profile__git_url', 'user__profile__ya_url', 'user__profile__vk_url', 'user__profile__ok_url',
                    'user__profile__bio')


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

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug']).select_related('cat', 'user')


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug']) \
            .values('title', 'body', 'time_created', 'user__username', 'user__id')


class CategoryView(ListView):
    model = Category
    template_name = 'blog/category_all.html'
    ordering = ('title',)


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


class PostsByCategory(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ('-time_created',)
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['slug']) \
            .values('title', 'slug', 'body', 'time_created', 'user__username', 'cat__title', 'cat__slug')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = self.kwargs['slug']
        return context


def search_blogs(request):
    if request.method == 'POST':
        searched = request.POST['searched']  # <input name="searched" ...
        q = Q(title__icontains=searched) | Q(body__icontains=searched)
        object_list = Post.objects.filter(q) \
            .values('title', 'slug', 'body', 'time_created', 'user__username', 'cat__title', 'cat__slug')
        return render(request, 'blog/post_search.html', {'object_list': object_list, 'search_key': searched})
    return render(request, 'blog/post_search.html', {})


class PostsByUser(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ('-time_created',)
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user) \
            .values('title', 'slug', 'body', 'time_created', 'user__username', 'cat__title', 'cat__slug')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 'user'
        return context
