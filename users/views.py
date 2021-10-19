from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

from users.models import User
from users.forms import CreateUserForm, LoginForm

# Create your views here.
class CreateUserView(View):
    template_name = 'signup.html'
    form = CreateUserForm()

    def get(self, request):
        return render(request, self.template_name, { "form": self.form, "header": "Signup" })

    def post(self, request):
        form = CreateUserForm(request.POST)
        username = form.data.get('username')
        
        if User.objects.filter(username=username).exists():
            e = u'Username "%s" is already in use.' % username
            return render(request, self.template_name, {"form": self.form, "error": e, "header": "Signup" })

        elif form.data['password1'] != form.data['password2']:
            e = "The provided passwords did not match."
            return render(request, self.template_name, {"form": self.form, "error": e, "header": "Signup" })
        
        elif form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
            username=data.get('username'),
            password=data.get('password1')
            )
            return redirect(reverse('login'))

        e = "Something went wrong with your password. Check the instructions above and try again."
        return render(request, self.template_name, { "form": self.form, "error": e, "header": "Signup" })


class LoginView(View):
    template_name = 'login.html'
    form = LoginForm()
    
    def get(self,request):
        return render(request, self.template_name, {"form": self.form, "header": "Login"})

    def post(self, request):
        form = LoginForm(request.POST)
        username = form.data.get('username')
        
        if not User.objects.filter(username=username).exists():
                e = u'Username "%s" does not exist.' % username
                return render(request, self.template_name, {"form": self.form, "error": e, "header": "Login"})
        
        elif form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, 
                username=data.get("username"),
                password=data.get("password")
            )
            if user:
                login(request, user)
                return redirect(reverse("homepage"))
        
        e = "That username and password did not match."
        return render(request, self.template_name, { "form": self.form, "error": e, "header": "Login" })      
    

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("login"))