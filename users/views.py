from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


from users.models import User
from users.forms import CreateUserForm, LoginForm

# Create your views here.

class CreateUserView(View):
  template_name = 'signup.html'
  form = CreateUserForm()

  def get(self, request):
    return render(request, self.template_name, { "form": self.form })

  def post(self, request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      user = User.objects.create_user(
        username=data.get('username'),
        password=data.get('password1')
        )
      return redirect(reverse('login'))

    return render(request, self.template_name, { "form": self.form })

class LoginView(View):
  
  def post(self,request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"),
                password=data.get("password")
            )
            if user:
                login(request, user)
                return redirect(reverse("signup"))
    form = LoginForm()
    return render(request, "login_form.html", {"form": form})      
    
  def get(self,request):
    template_name = 'login.html'
    form = LoginForm()
    return render(request, template_name, {"form": form, "header": "Login"})


def logout_view(request):
    logout(request)
    return redirect(reverse("homepage"))
