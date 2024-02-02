from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render (request, "player/index.html", {
        "user":request.user,
    })

def register_user(request):
    if request.method == 'POST':
        # Get user input from the registration form
        username = request.POST.get('reg_username')
        password = request.POST.get('reg_password')
        email = request.POST.get('reg_email')

        # Check if the username is unique
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('index')

        # Create a new user instance
        new_user = User(username=username, email=email)

        # Set the password for the user (you should hash the password before saving in a real-world scenario)
        new_user.set_password(password)

        # Save the user instance to the database
        new_user.save()

        messages.success(request, 'Account created successfully.')

        return redirect('index')

    return redirect("index")

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('index')  # Redirect to your home page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'player/index.html', {'form': form, "user": request.user,})
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Redirect to your login page
