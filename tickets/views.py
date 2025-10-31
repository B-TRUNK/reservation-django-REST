from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status, filters, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
#Customized Permissions
from .permissions import IsAuthorOrReadOnly




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


#@ Way_1 - Function Based Views
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
    
# 3.2 (GET, PUT, DELETE)
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_id(request, id):

    try:
        guest = Guest.objects.get(id=id)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    #GET
    if request.method == 'GET':
        serializer = GuestSerlializer(guest)
        return Response(serializer.data)
    #PUT
    elif request.method == 'PUT':
        serializer = GuestSerlializer(guest, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#@ Way_2 - Class Based Views

# 4.1 List & Create = GET & POST
class CBV_List(APIView):
    
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerlializer(guests, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GuestSerlializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST) 
    

# 4.2 GET PUT DELETE class based views -- id
class CBV_id(APIView):

    def get_object(self, id):
        try:
            return Guest.objects.get(id=id)
        except Guest.DoesNotExist:
            raise Http404
    #get
    def get(self, request, id):
        guest = self.get_object(id)
        serializer = GuestSerlializer(guest)
        return Response(serializer.data)
    
    #put
    def put(self, request, id):
        guest = self.get_object(id)
        serializer = GuestSerlializer(guest ,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #delete
    def delete(self, request, id):
        guest = self.get_object(id)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# 5-1 makesense(mixins) rest view
# it is an extend for CBV
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerlializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
# 5-2 makesense(mixins) get, put, delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerlializer

    def get(self, request, pk):
        return self.retrieve(request)
    
    def put(self, request, pk):
        return self.update(request)
    
    def delete(self, request, pk):
        return self.destroy(request)
    

# 6 - 1 Generics GET, PUST
class Generics_List(generics.ListCreateAPIView):
    queryset                = Guest.objects.all()
    serializer_class        = GuestSerlializer
    authentication_classes  = [TokenAuthentication]
    permission_classes      = [IsAuthenticated]



# 6 - 2 Generics GET, PUST
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset                = Guest.objects.all()
    serializer_class        = GuestSerlializer
    authentication_classes  = [TokenAuthentication]
    permission_classes      = [IsAuthenticated]


# 7 - 1 Viewsets GET, PUST
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerlializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerlializer


#--------------------------------------------

# 8 - Find Movie
@api_view(['GET'])
def find_movie(request):
    movie = request.query_params.get('movie')
    hall = request.query_params.get('hall')

    # Use filter if multiple movies could exist with same hall
    movies = Movie.objects.filter(movie=movie, hall=hall)

    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# Create Reservations
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        movie = request.data['movie'],
        hall = request.data['hall'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)


# 12 -  Post Author Editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer





