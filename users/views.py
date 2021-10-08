from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from users.models import User
from users.forms import CreateUserForm

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
    return redirect(reverse("signup"))

    return render(request, self.template_name, { "form": self.form })
