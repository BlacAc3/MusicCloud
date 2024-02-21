import contextlib
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
import imghdr
from google.cloud import storage
from django.conf import settings
import os
from .models import *

# google cloud setup 
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()


# Create your views here.
def index(request): 
    audios = Audio.objects.filter(user=request.user.id).order_by("-date_created")
    playing = audios.first() if audios else None
    return render (request, "player/index.html", {
        "user":request.user,
        "audios":audios,
        "playing":playing,
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

def save_audio(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']
        # Check if file exists
        possible_audio=Audio.objects.filter(title=uploaded_file.name).exists()
        if possible_audio:
            return redirect('index')  # Redirect to a success page
        # check if file is an audio 
        if uploaded_file.content_type != "audio/mpeg":
            return redirect("index")
        
            
        # if not create or upload one 
        audio_instance = Audio.objects.create(user=request.user, title=uploaded_file.name)
        

        # Upload file to Google Cloud Storage
        storage_client = storage.client.from_service_account_json(settings.GS_JSON_KEY_FILE)
        bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(audio_instance.get_cloud_name())
        blob.upload_from_file(uploaded_file.file)
        audio_instance.save()
        return redirect("index")
    

@csrf_exempt
def handle_uploaded_file(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']

        # Check if file exists
        possible_audio=Audio.objects.filter(title=uploaded_file.name).exists()
        if possible_audio:
            return JsonResponse({"message":"file already exists"})
        # check if it is an audio file
        if uploaded_file.content_type != "audio/mpeg":
            return JsonResponse({"message":f"File is an --{uploaded_file.content_type}-- and not an audio file "})
        
        # if not create or upload one 
        audio_instance = Audio.objects.create(user=request.user, title=uploaded_file.name)

        # Upload file to Google Cloud Storage
        storage_client = storage.client.from_service_account_json(settings.GS_JSON_KEY_FILE)
        bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(audio_instance.get_cloud_name())
        blob.upload_from_file(uploaded_file.file)
        audio_instance.save()


        return JsonResponse({'message': f"--{uploaded_file.name}-- has been received"})
    else:
        return JsonResponse({'message': 'No file received.'})

def play(request, id):
    if not Audio.objects.filter( id=id).exists():
        return redirect("index")
    playing = Audio.objects.get(id=id)
    audios = Audio.objects.all().order_by("-date_created")
    user=request.user
    return render(request, "player/index.html", {
        "playing":playing,
        "audios":audios,
        "user":user,
    })

def delete_audio(request, id):
    if not Audio.objects.filter(id=id).exists():
        return redirect("index")
    playing = Audio.objects.get(id=id)

    storage_client = storage.client.from_service_account_json(settings.GS_JSON_KEY_FILE)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(playing.get_cloud_name())
    try:
        blob.delete()
    except:
        pass
    playing.delete()
    return redirect("index")
