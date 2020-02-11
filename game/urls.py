from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('rooms', views.rooms, name='rooms'),
    path('<str:room_name>/', views.room, name='room'),
]