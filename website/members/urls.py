from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import UserRegistrationView, UserChangeView, UserPasswordChangeView, password_changed


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('edit-user/', UserChangeView.as_view(), name='edit-user'),

    # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('password/', UserPasswordChangeView.as_view(template_name='registration/change_password.html'),
         name='change-password'),
    path('password-success/', password_changed, name='password-changed'),   # переадресация после смена пароля

]
