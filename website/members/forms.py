from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(UserCreationForm):
    """ Стилизуем форму регистрации пользователя. """
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Не более 150 символов. Только буквы, '
                                                                            'цифры и символы @/./+/-/_.'}),
                               label='Логин пользователя')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label='Имя')
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

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
    last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label='Последний раз был')
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
        fields = ('username', 'first_name', 'last_name', 'email', 'password',
                  'last_login')


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
