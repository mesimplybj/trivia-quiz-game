from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def rooms(request):
    return render(request, 'rooms.html')

def home(request):
    return render(request, 'base.html')

def room(request, room_name):
    return render(request, 'base.html', { 'room_name': room_name})