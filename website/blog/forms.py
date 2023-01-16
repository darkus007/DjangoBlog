from django import forms

from website.utilites import slugify
from .models import Post


class PostForm(forms.ModelForm):

    def clean_slug(self):
        """
        Не запускается, если поле "slug" пустое!!!
        По этой причине оно скрыто и добавлено значение none.
        """
        return slugify(self.cleaned_data['title'])

    class Meta:
        model = Post
        fields = ('cat', 'title', 'slug', 'body')

        widgets = {
            # 'user': forms.Select(attrs={'class': 'form-control'}),
            'cat': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Наименование поста'}),
            # метод clean_slug не запускается, если поле "slug" пустое,
            # по этой причине оно скрыто и добавлено значение "none".
            'slug': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'URL-адрес поста (slug)',
                                           'value': 'none', 'type': 'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
