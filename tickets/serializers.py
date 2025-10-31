from rest_framework import serializers
from tickets.models import *


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReservationSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class GuestSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'reservation', 'guest', 'mobile']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


#uuid  slog