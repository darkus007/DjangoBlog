from django.urls import reverse_lazy
from django.views import generic
# from django.contrib.auth.forms import UserCreationForm

from .forms import UserRegistrationForm


class UserRegistrationView(generic.CreateView):
    # form_class = UserCreationForm
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
