from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from google.cloud import storage
import os
import uuid


class Category(models.Model):
    category_name = models.CharField(max_length=30)
    is_deleted = models.BooleanField(default=False)

class Book(models.Model):
    title = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    publisher = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

class Member(models.Model):
    member_id = models.CharField(max_length=30, primary_key=True)
    member_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)

class Borrow(models.Model):
    borrow_id = models.CharField(max_length=30, primary_key=True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    borrow_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True)
    borrow_status = models.CharField(max_length=15)

class Role(models.Model):
    role_name = models.CharField(max_length=30)

class Audio(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="musics")
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.TextField()
    date_created=models.DateTimeField(default=timezone.now)

    def get_cloud_name(self):
        return f"{self.id}{self.title}"

    def get_audio_url(self):
        # Create a GCS client
        storage_client = storage.Client.from_service_account_json(settings.GS_JSON_KEY_FILE)
        # Get the bucket
        bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
        # Construct the path to the file within the bucket
        blob = bucket.blob(self.get_cloud_name())
        return blob.public_url

    def get_music_name(self):
        parts = str(self.title).split('-')
        new_name = " ".join(parts)
        name = str(parts).split("_")

        return new_name