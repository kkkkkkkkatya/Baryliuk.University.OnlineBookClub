from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Session(models.Model):
    room_name=models.CharField(max_length=300, blank=False)
    date_start = models.CharField(max_length=30, blank=False)
    date_end=models.CharField(max_length=30, blank=False)
    author = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.room_name)


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name
