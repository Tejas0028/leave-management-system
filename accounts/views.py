from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from accounts.forms import LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            return redirect("login")
    return render(request,"register.html",{"form" :form})


def login_page(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)

                if user.role == 2:
                    return redirect("dashboard")
                else:
                    return redirect("dashboard")

            else:
                return render(request, "templates/login.html", {
                    "form": form,
                    "error": "Invalid email or password"
                })

    return render(request, "login.html", {
        "form": form
    })


@login_required
def dashboard(request):
    user = request.user

    return render(request, "dashboard.html", {
        "user": user
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")