from django.urls import path
from .views import UserRegistrationView, UserChangeView, UserPasswordChangeView, password_changed,\
    UserProfileView, CreateUserProfileView, EditUserProfileView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('edit-user/', UserChangeView.as_view(), name='edit-user'),

    path('password/', UserPasswordChangeView.as_view(template_name='registration/change_password.html'),
         name='change-password'),
    path('password-success/', password_changed, name='password-changed'),

    path('profile/<slug:slug>/', UserProfileView.as_view(), name='user-profile'),
    path('create-profile/', CreateUserProfileView.as_view(), name='user-profile-create'),
    path('update-profile/<slug:slug>/', EditUserProfileView.as_view(), name='user-profile-update'),
]
