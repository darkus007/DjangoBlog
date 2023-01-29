from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.views import PasswordChangeView
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .forms import UserRegistrationForm, EditUserForm, UserPasswordChangeForm, ProfilePageForm
from .models import Profile

from website.utilites import slugify


class UserRegistrationView(CreateView):
    # form_class = UserCreationForm
    form_class = UserRegistrationForm
    template_name = 'registration/register_or_edit_user.html'   # шаблон по умолчанию register.html
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый пользователь'
        context['button'] = 'Регистрация'
        context['extra_link'] = False
        return context


class UserChangeView(UpdateView):
    # form_class = UserChangeForm
    form_class = EditUserForm
    template_name = 'registration/register_or_edit_user.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """
        Переопределяем метод для заполнения формы
        данными текущего авторизованного пользователя.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать пользователя'
        context['button'] = 'Обновить профиль'
        context['extra_link'] = True
        return context


class UserPasswordChangeView(PasswordChangeView):
    # form_class = PasswordChangeForm
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('password-changed')      # перенаправление на кастомную страницу


def password_changed(request):
    return render(request, 'registration/password_changed.html')


# классы представления для Profile:

class UserProfileView(DetailView):
    model = Profile
    template_name = 'registration/user_profile_show.html'

    def get_queryset(self):
        return Profile.objects.filter(slug=self.kwargs['slug']) \
            .values('user__first_name', 'user__last_name', 'image', 'bio',
                    'ya_url', 'vk_url', 'ok_url', 'git_url', 'website_url')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_profile = get_object_or_404(Profile, slug=self.kwargs['slug'])
    #     context['user_profile'] = user_profile
    #     return context


class CreateUserProfileView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/user_profile_create_update.html'
    # fields = '__all__'  # поля теперь прописаны в ProfilePageForm

    def form_valid(self, form):
        """ Передаем пользователя в форму """
        form.instance.user = self.request.user
        form.instance.slug = slugify(str(self.request.user.username) + '-profile')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать страницу профиля'
        context['button'] = 'Создать страницу профиля'
        context['extra_msg'] = 'для создания профиля.'
        return context


class EditUserProfileView(UpdateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/user_profile_create_update.html'
    # fields = ['bio', 'image', 'website_url', 'git_url', 'ya_url', 'vk_url', 'ok_url']
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновить страницу профиля'
        context['button'] = 'Обновить страницу профиля'
        context['extra_msg'] = 'для обновления профиля.'
        return context
