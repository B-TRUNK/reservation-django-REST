"""
URL configuration for restb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reserves', views.viewsets_reservation)


urlpatterns = [
    path('admin/', admin.site.urls),

    # 1
    path('django/jsonresponsenomodel/', views.no_rest_no_model),

    # 2
    path('django/jsonresponsefrommodel/', views.no_rest_from_model),

    # 3.1 (REST_POST, REST_GET)
    path('rest/fbv/', views.FBV_LIST),
    
    # 3.2 (REST_GET, PUT, DELETE)
    path('rest/fbv/<int:id>', views.FBV_id),
    
    # 4.1 (CBV_get_post)
    path('rest/cbv/', views.CBV_List.as_view()),

    # 4.2 (CBV_get_put_delete)
    path('rest/cbv/<int:id>', views.CBV_id.as_view()),

    # 5.1 (mixins_get_post)
    path('rest/mixins/', views.mixins_list.as_view()),

    # 5.2 (mixins_get_put_delete)
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),

    # 6.1 (generics_get_post)
    path('rest/generic/', views.Generics_List.as_view()),

    # 6.2 (generics_get_put_delete)
    path('rest/generic/<int:pk>', views.Generics_pk.as_view()),

    # 7.1 (viewsets_get_post)
    path('rest/viewsets/', include(router.urls)),

    # 8 - Find Movies
    path('fbv/findmovie/', views.find_movie),

    # 9 - New Reservation
    path('fbv/newreserv/', views.new_reservation),

    # 10 - REST AUTH url
    path('api_auth/', include('rest_framework.urls')), #to add a logout option

    # 11 - Token Authentication
    path('api-token-auth/', obtain_auth_token),

    #12 - Post pk Generics
    #path('post/generic/',include(views.Post_List.as_view()) ),
    path('post/generic/<int:pk>',views.Post_pk.as_view()),
]
