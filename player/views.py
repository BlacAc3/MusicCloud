################ Importing Modules ########################
import contextlib
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
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


####### google cloud setup ########
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

####### Initializing Index ##############
def index(request, **kwargs):
    audios = Audio.objects.filter(user=request.user.id).order_by("-date_created")
    playing = audios.first() if audios else None
    message = kwargs["message"] if kwargs else None
    return render (request, "player/index.html", {
        "user":request.user,
        "audios":audios,
        "playing":playing,
        "message":message,
    })



######## Creating Registration Function ##############
def register_user(request):
    ######### Verifying Request ############
    if request.method != "POST":
        return redirect("index")
    ######## Getting User Form Input ##############
    username :str = request.POST.get('reg_username').lower()
    password :str = request.POST.get('reg_password')
    email = request.POST.get('reg_email')
    ######## Checking username uniqueness ##########
    if User.objects.filter(username=username).exists():
        return index(request, message='Username is already taken.')
    ######## Creating new user ##########
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    new_user.save()
    return index(request, message = 'Account created successfully.')


########### Handling Login ##############
def login_user(request):
    if request.method != 'POST':
        return index(request, message ="Invalid username or password.")
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        return _extracted_from_login_user_(form, request)
    return index(request, message = "User not Found")



########## Verifying User login #############
def _extracted_from_login_user_(form, request):
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is None:
        return index(request, message='Invalid username or password.')
    login(request, user)
    return index(request, message=f"Welcome {username}")  # Redirect to your home page



############# Logging out User ##############
@login_required
def logout_user(request):
    logout(request)
    return index(request, message='You have been logged out successfully.')



########## Handling Audio Upload from "click" ################
def save_audio(request):
    if request.method != 'POST' or not request.FILES:
        return index(request, message="An Error Occured")
    ######## Initializing Uploaded Files #########
    uploaded_file = request.FILES['file']

############### Running Checks ##################
    ### Checking database for Audio! ###
    if possible_audio := Audio.objects.filter(title=uploaded_file.name).exists():
        return index(request, message="Music already exists!")  # Redirect to a success page
    ### Checking if file is an audio ### 
    if uploaded_file.content_type != "audio/mpeg":
        return index(request, message="Song format not supported!!")
    ### Checking if File is less than 4.1mb ### (Restriction by hosting service "Vercel.com")
    if uploaded_file.size > 4_100_000:
        return index(request,  message="File too large! File should be below 4.2mb!")

############### Handling Upload! ################
    ##### Updating Database ###### 
    audio_instance = Audio.objects.create(user=request.user, title=uploaded_file.name)
    ##### Uploading file to Google Cloud Storage #####
    storage_client = storage.client.from_service_account_json(settings.GS_JSON_KEY_FILE)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(audio_instance.get_cloud_name())
    blob.upload_from_file(uploaded_file.file)
    audio_instance.save()
    return index(request, message="Uploaded succesfully!")



############# Handling Upload From Drag'n'Drop ############
@csrf_exempt
def handle_uploaded_file(request):
    if request.method != 'POST' or not request.FILES:
        return JsonResponse({'message': 'No file received.'})
    uploaded_file = request.FILES['file']

############### Running Checks ###########################
    ###### Checking if audio exists #######
    if possible_audio := Audio.objects.filter(title=uploaded_file.name).exists():
        return JsonResponse({"message":"file already exists"})
    ###### Confirming file type is Audio #######
    if uploaded_file.content_type != "audio/mpeg" or uploaded_file.content_type != "audio/mp3" or uploaded_file.content_type != "audio/wav" or uploaded_file.content_type != "audio/ogg" or uploaded_file.content_type != "audio/m4a":
        return JsonResponse({"message":f"File is an --{uploaded_file.content_type}-- and not an audio file "})
    ###### Checking if File is less than 4.1mb  (Restriction by hosting service "Vercel.com") #######
    if uploaded_file.size > 4_000_000:
        return index(request,  message="File too large! File should be below 4mb!")
    
################# Handling Upload ####################
    ####### Updating database ########
    audio_instance = Audio.objects.create(user=request.user, title=uploaded_file.name)
    ####### Uploading file to Google Cloud Storage #########
    storage_client = storage.client.from_service_account_json(settings.GS_JSON_KEY_FILE)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(audio_instance.get_cloud_name())
    blob.upload_from_file(uploaded_file.file)
    audio_instance.save()
    return JsonResponse({'message': f"--{uploaded_file.name}-- has been received"})



########## Rendering Selected Audio ###########
def play(request, id):
    ####### Checking if Audio Exists ########
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



########## Deleting Selected Audio #############
def delete_audio(request, id):
    ####### Checking if Audio Exists ########
    if not Audio.objects.filter(id=id).exists():
        return index(request, message = "Song doesn't exist!")
    playing = Audio.objects.get(id=id)
    song_name=playing.get_music_name()
    storage_client = storage.client.from_service_account_json(settings.GS_JSON_KEY_FILE)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(playing.get_cloud_name())
    
    ### If during deletion in cloud if errors(file not found) continue to update the database 
    try:
        blob.delete()
    except:
        pass
    playing.delete()
    return index(request, message=f"{song_name} deleted!")
