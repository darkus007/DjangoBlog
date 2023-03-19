from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.core.mail import mail_admins
from django.core.cache import cache

from website.settings import ALL_CATEGORIES, PAGINATE_BY_CONST
from .models import Post, Category
from .forms import PostForm, CategoryForm, SendToStaffForm


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ('-time_created',)
    paginate_by = PAGINATE_BY_CONST

    def get_queryset(self):
        return Post.objects.values('title', 'slug', 'body', 'time_created', 'user__username', 'cat__title', 'cat__slug')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = ALL_CATEGORIES.get('slug')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug']) \
            .values('title', 'slug', 'body', 'time_created', 'user__username', 'cat__title', 'user__id',
                    'user__first_name', 'user__last_name', 'user__profile__image', 'user__profile__website_url',
                    'user__profile__git_url', 'user__profile__ya_url', 'user__profile__vk_url', 'user__profile__ok_url',
                    'user__profile__bio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = post.total_likes()

        liked = False
        if post.likes.filter(pk=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


def like_post(requests, slug):
    post = get_object_or_404(Post, slug=requests.POST.get('post_slug'))  # <button type="submit" name="post_slug" ...
    if post.likes.filter(pk=requests.user.id).exists():
        post.likes.remove(requests.user)
    else:
        post.likes.add(requests.user)
    # перенаправление на ту же страницу
    return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_add.html'
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

    def form_valid(self, form):
        """ Чистим кэш categories для их преративного обновления на странице """
        cache.delete('categories')
        return super().form_valid(form)


class UpdateCategoryView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_update.html'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        """ Чистим кэш categories для их преративного обновления на странице """
        cache.delete('categories')
        return super().form_valid(form)


class DeleteCategoryView(DeleteView):
    model = Category
    template_name = 'blog/category_delete.html'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        """ Чистим кэш categories для их преративного обновления на странице """
        cache.delete('categories')
        return super().form_valid(form)


class PostsByCategory(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ('-time_created',)
    paginate_by = PAGINATE_BY_CONST

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
    paginate_by = PAGINATE_BY_CONST

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user) \
            .values('title', 'slug', 'body', 'time_created', 'user__username', 'cat__title', 'cat__slug')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 'user'
        return context


def send_email_to_staff(request):
    if request.method == 'POST':
        form = SendToStaffForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data['body'] + '\n' + request.user.email
            mail_admins(form.cleaned_data['title'], msg,
                        fail_silently=False, connection=None, html_message=None)
            return redirect('send-email-success')
    else:
        form = SendToStaffForm()

    return render(request, 'blog/send_email.html', {'form': form})


def send_email_to_staff_success(request):
    return render(request, 'blog/send_email_success.html')


def pageNotFound(request, exception):
    return render(request, 'blog/base.html')
