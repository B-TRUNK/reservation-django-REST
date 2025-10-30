from django.db import models

# guests, movie, reservation

class  Movie(models.Model):
    movie_name      = models.CharField(max_length=50, default=False, blank=False)
    hall            = models.CharField(max_length=50, default=False, blank=False)
    data            = models.DateField(False, auto_now_add=False)


    def __str__(self):
        return self.movie_name
    

class Guest(models.Model):
    guest_name      = models.CharField(max_length=30)
    mobile          = models.CharField(max_length=10)


    def __str__(self):
        return self.mobile
    



class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)
