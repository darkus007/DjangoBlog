from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .forms import UserRegistrationForm, EditUserForm, UserPasswordChangeForm


class UserRegistrationView(generic.CreateView):
    # form_class = UserCreationForm
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserChangeView(generic.UpdateView):
    # form_class = UserChangeForm
    form_class = EditUserForm
    template_name = 'registration/edit_user.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """
        Переопределяем метод для заполнения формы
        данными текущего авторизованного пользователя.
        """
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    # form_class = PasswordChangeForm
    form_class = UserPasswordChangeForm
    # success_url = reverse_lazy('home')
    success_url = reverse_lazy('password-changed')      # перенаправление на кастомную страницу


def password_changed(request):
    return render(request, 'registration/password_changed.html')
