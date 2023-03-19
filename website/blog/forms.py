from django import forms
from website.settings import EMAIL_THEME_CHOICES

from captcha.fields import CaptchaField

from .models import Post, Category
from website.utilites import slugify


class PostForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки',
                           error_messages={'invalid': 'Неверно указан текст с картинки'})

    def clean_slug(self):
        """
        Не запускается, если поле "slug" пустое!!!
        По этой причине оно скрыто и добавлено значение none.
        """
        return slugify(self.cleaned_data['title'])

    class Meta:
        model = Post
        fields = ('cat', 'title', 'slug', 'body', 'captcha')

        widgets = {
            'cat': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Укажите название поста'}),
            # метод clean_slug не запускается, если поле "slug" пустое,
            # по этой причине оно скрыто и добавлено значение "none".
            'slug': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'URL-адрес поста (slug)',
                                           'value': 'none', 'type': 'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    def clean_slug(self):
        """
        Не запускается, если поле "slug" пустое!!!
        По этой причине оно скрыто и добавлено значение none.
        """
        return slugify(self.cleaned_data['title'])

    class Meta:
        model = Category
        fields = ('title', 'slug')

        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'}),
                   'slug': forms.TextInput(
                       attrs={'class': 'form-control', 'placeholder': 'URL-адрес поста (slug)', 'value': 'none',
                              'type': 'hidden'}), }


class SendToStaffForm(forms.Form):
    """ Форма для отправки e-mail сообщений администратору сайта """
    title = forms.ChoiceField(label='Тема обращения',
                              choices=EMAIL_THEME_CHOICES,
                              widget=forms.Select(attrs={'class': 'form-control', 'label': 'Название категории'}))
    body = forms.CharField(label='Текст обращения',
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Введите текст с картинки',
                           error_messages={'invalid': 'Неверно указан текст с картинки'})
