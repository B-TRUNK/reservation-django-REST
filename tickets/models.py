from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings 
from django.contrib.auth.models import User

# guests, movie, reservation

class  Movie(models.Model):
    movie           = models.CharField(max_length=50, default=False, blank=False)
    hall            = models.CharField(max_length=50, default=False, blank=False)
    #date           = models.DateField(False, auto_now_add=False)


    def __str__(self):
        return self.movie
    

class Guest(models.Model):
    guest           = models.CharField(max_length=30)
    mobile          = models.CharField(max_length=10)


    def __str__(self):
        return self.mobile
    



class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()


# Create auto generated token for each created new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_create_token_create(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)