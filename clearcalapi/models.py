from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)
    all_day = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')


class UserSubClass(models.Model):
    USER_TYPES = [
        ('VL', 'volunteer'),
        ('OG', 'organization'),
    ]

    type = models.CharField(max_length=32,  choices=USER_TYPES)

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserSubClass.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.usersubclass.save()


class Shift(models.Model):
    start = models.CharField(max_length=16)
    end = models.CharField(max_length=16)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='shifts')
    volunteer = models.ForeignKey(UserSubClass, on_delete=models.CASCADE, related_name='shifts', default=None)

