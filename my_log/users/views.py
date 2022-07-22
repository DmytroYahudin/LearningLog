from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

# Create your views here.


class SignUpView(CreateView):
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse("my_notes:index"))
