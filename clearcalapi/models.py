from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)
    all_day = models.BooleanField(default=False)
    start = models.CharField(max_length=16)
    end = models.CharField(max_length=16)

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

