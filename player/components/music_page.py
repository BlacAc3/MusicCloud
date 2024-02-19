from django_unicorn.components import UnicornView
from player.models import Audio

class MusicPageView(UnicornView):
    comp_audios = Audio.objects.none()
    user_playing = None
    
    def mount(self):
        self.comp_audios= Audio.objects.all().order_by("-date_created")
        self.user_playing=None
    def play(self, id):
        playing = Audio.objects.get(id=id)
        self.mount()
        self.user_playing = playing if Audio.objects.filter(id=id).exists() else None