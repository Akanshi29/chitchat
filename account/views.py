from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login-user')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('active-users')
    else:
        return render(request, "account/loginPage.html", {})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect("login-user")
    