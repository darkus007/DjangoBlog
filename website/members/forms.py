from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django import forms

from captcha.fields import CaptchaField

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    """ Стилизуем форму регистрации пользователя. """
    # username = forms.CharField(max_length=150,
    #                            widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                          'placeholder': 'Не более 150 символов. Только буквы, '
    #                                                                         'цифры и символы @/./+/-/_.'}),
    #                            label='Логин')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label='Имя')
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Фамилия')
    captcha = CaptchaField(label='Введите текст с картинки',
                           error_messages={'invalid': 'Неверно указан текст с картинки'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'captcha')
        labels = {'username': 'Логин'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class EditUserForm(UserChangeForm):
    """ Стилизуем форму обновления профиля пользователя. """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Имя')
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Фамилия')
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Логин')
    # last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
    #                              label='Последний раз был')
    # is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
    #                                label='Суперпользователь')
    # is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
    #                            label='Персонал')
    # is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
    #                             label='Активен')
    # date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
    #                               label='Дата регистрации')

    class Meta:
        model = User
        # fields = ('username', 'first_name', 'last_name', 'email', 'password',
        #           'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserPasswordChangeForm(PasswordChangeForm):
    """ Стилизуем форму смены пароля пользователя. """
    old_password = forms.CharField(max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
                                   label='Старый пароль')
    new_password1 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
                                    label='Новый пароль')
    new_password2 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
                                    label='Подтверждение нового пароля')

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
        # fields = '__all__' - что бы вернуть комментарии к паролю, напишем их в шаблоне change-password.html


class ProfilePageForm(forms.ModelForm):
    """ Формы для классов представления Profile """
    class Meta:
        model = Profile
        fields = ['bio', 'image', 'website_url', 'git_url', 'ya_url', 'vk_url', 'ok_url']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Краткая информация о себе'}),
            # 'image': forms.ModelChoiceField(attrs={'class': 'form-control'}),
            'ya_url': forms.TextInput(attrs={'class': 'form-control'}),
            'vk_url': forms.TextInput(attrs={'class': 'form-control'}),
            'ok_url': forms.TextInput(attrs={'class': 'form-control'}),
            'git_url': forms.TextInput(attrs={'class': 'form-control'}),
            'website_url': forms.TextInput(attrs={'class': 'form-control'}),
        }
