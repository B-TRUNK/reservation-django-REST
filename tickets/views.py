from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *


# references for views serialization
#===================================


# 1 - without REST or model query FBV

def no_rest_no_model(request):
    guests = [
        {
            'id' : 1,
            'name' : 'omar',
            'mobile' : '65651613'
        },
        {
            'id' : 2,
            'name' : 'noue',
            'mobile' : '7678643'
        }
    ]
    return JsonResponse(guests, safe=False) #no hashing for data

# 2 - No REST ,but from model
def no_rest_from_model(request):
    data = Guest.objects.all()

    response = {
        'guests' : list(data.values('guest_name', 'mobile'))
    }
    return JsonResponse(response)