from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("login", views.login_user, name="login"),
    path("register", views.register_user, name="register"),
    path("logout", views.logout_user,name = "logout" ),
    path("save-audio", views.save_audio, name="save_audio"),
    path("drag-drop", views.handle_uploaded_file, name="drag-drop"),
    path("play_audio<int:id>", views.play, name="play"),
    path("delete_audio<int:id>", views.delete_audio, name="delete_audio"),
]

