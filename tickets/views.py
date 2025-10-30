from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status, filters
from rest_framework.response import Response


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

# 3.1 (GET, POST)

@api_view(['GET', 'POST'])
def FBV_LIST(request):

    #GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerlializer(guests, many=True)
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        serializer = GuestSerlializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)