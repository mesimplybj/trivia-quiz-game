from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')

def rooms(request):
    return render(request, 'rooms.html')

def home(request):
    return render(request, 'base.html')

def chat(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    #return render(request, 'chat/room.html', { 'room_name': room_name})
    return render(request, 'base.html', { 'room_name': room_name})