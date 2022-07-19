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
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse('my_notes:index'))

# def register(request):
#     if request.method != 'POST':
#         form = UserCreationForm()
#     else:
#         form = UserCreationForm(data=request.POST)
#
#         if form.is_valid():
#             new_user = form.save()
#             authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
#             login(request, authenticated_user)
#             return HttpResponseRedirect(reverse('origin:index'))
#     context = {'form': form}
#     return render(request, 'users/register.html', context)


