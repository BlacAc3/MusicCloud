from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

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
    file = models.FileField(upload_to="audio/")
    title = models.TextField()
    date_created=models.DateTimeField(default=timezone.now)

    def get_audio_url (self):
        return self.file.url

    def get_music_name(self):
        name = os.path.basename(str(self.file.name)).split("_")

        return " ".join(name)