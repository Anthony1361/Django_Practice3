from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {"id" : 1, "name" : "Lets learn python!"},
#     {"id" : 2, "name" : "Design with me"},
#     {"id" : 3, "name" : "Frontend developers"},
# ]


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        #use try: to make sure the user actually exists ///
        try:
            #import models user at the top  ///
            user = User.objects.get(username=username)
            # user = User.objects.get(username="tina")
        except:
            #import messages at top ////
            messages.error(request,'User does not exist')  

            #if the user exists ///
            #import authenticate, login and login out method at the top ///
        user = authenticate(request, username=username, password=password)
        # user = authenticate(request, username="tina", password="12345678qwertyui")

        if user is not None:
            login(request, user)
            return redirect('home')   
        else:
            messages.error(request,'User OR Password does not exist')     

    context = {}
    return render(request, "home/login_register.html", context)

def homePage(request):
    q = request.GET.get("q")  if request.GET.get("q") != None else ""
    # rooms = Room.objects.filter(topic__name__icontains = q) 

    #remember to import Q at the top .........///////////
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all() 

    room_count = rooms.count()

    context = {'rooms': rooms, 'topics':topics, 'room_count': room_count}
    return render(request, 'home/index.html', context)

def roomPage(request, pk):
    room = Room.objects.get(id=pk)       
    context = {'room' : room}
    return render(request, 'home/room.html', context)

# def roomPage(request, pk):
#     room = None
#     for i in rooms:
#         if i ['id'] == int(pk):
#             room = i
#     context = {'room': room}        
#     return render(request, 'home/room.html', context)

def createRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            #dont forget to redirect at the top/////////
            return redirect("home")

    context = {"form":form}
    return render(request, "home/room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            #dont forget to redirect at the top/////////
            return redirect("home")


    context = {"form":form}
    return render(request, "home/room_form.html", context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "home/delete.html", {"obj":room})