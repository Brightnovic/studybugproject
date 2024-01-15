from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .functions import clean_username ,clean_email
from .forms import RoomForm, UserForm ,MyUserCreationForm

 
def custom_404_view(request, exception):
    title = "page not found!"
    context = {'title': title}
    return render(request, '404.html',context ,status=404)




def check_404(request):
    return render(request, 'base/404.html' )







def home(request):
    title = "Home page"
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) |
        Q(name__icontains= q)|
        Q(description__icontains= q)
 
                                )[0:5]
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    context = {"rooms": rooms , 'topics': topics,
                'room_count': room_count,
                'room_messages': room_messages,
                'title': title

                }
    return render(request, "base/home.html", context)


def room(request, pk):
    title = "Chat Room"
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() 
    participants = room.participants.all()
    if request.method == 'POST':
        message  = Message.objects.create(
            body = request.POST.get('body'),
            user = request.user,
            room=room
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {"room": room, 'room_messages': room_messages, 'participants': participants, 'title': title}
    return render(request, "base/room.html", context)
 
def LoginPage(request):
    title = "Login or Signup "
    page = 'login'
    context = {'page': page, 'title': title}
    if request.user.is_authenticated:
        messages.error(request, "Apologies You're Already Logged in!  ")
        return redirect('home')
    if request.method == "POST":

        email = request.POST.get("email").lower()
        password =request.POST.get("password")
        try:
            user = User.objects.get(email=email)
             
        except:
             
            messages.error(request, "email doesn't exist! please try again")
        user = authenticate(request, email=email,password=password)
         
        if user is not None:

            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Password doesn't exist! check and try again")

    return render(request, 'base/login_register.html' , context)





def logoutUser(request):
 
    logout(request)
    return redirect('home',)


def registerPage(request):
    page = 'register'
    title = "Login or Signup "
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            username = form.cleaned_data['username'].lower()
            if " " in username:
                messages.error(request, "make sure your username doesn't contain a white space")
            user.username = username   
            user.save()
            
            #user = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, f" the form you submitted  isn't valid make sure that your username  doesn't contain a space and email haven't been used before ")
    context = {'page': page , 'form': form, 'title': title}
    return render(request, 'base/login_register.html', context)




@login_required(login_url='login')
def createRoom(request):
    title = "Create a Room"
    form = RoomForm()
    topics = Topic.objects.all()
    create = "create"
    context = {'form': form, 'create': create, 'topics': topics, 'title': title}
    
    if request.method == 'POST':
       topic_name = request.POST.get('topic')
       topic , created = Topic.objects.get_or_create(name=topic_name)
       Room.objects.create(
           host=request.user,
           topic=topic,
           name=request.POST.get('name'),
           description =request.POST.get('description')

       )
       return redirect('home')
 

    return render (request,'base/room_form.html', context)


def userProfile(request,pk):
    title = "Profile"
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()[0:6]
    room_messages = user.message_set.all()[0:5]
    topics = Topic.objects.all()[0:5]
    context = {'user':user , 
               'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics,
               'title': title
               }
    
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def UpdateRoom(request, pk):
    title = "Update your room"
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error(request, "Sorry! you're not  the foundation! and can't   update! this room")
        return redirect(  'home')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)# instance is just like id the room passed in is for id detecting the room tp update
        room.name = request.POST.get('name')
        room.topic =  topic
        room.description = request.POST.get('description')
        room.save()
         
        return redirect('home')
    context = {'form': form, 'topics':topics, 'room':room, 'title': title}
    return render(request, 'base/room_form.html',context  )


@login_required(login_url='login')
def deleteRoom(request, pk):
    title = "Delete Room"
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        messages.error(request, "Sorry! you're not  the foundation! and can't   delete! this room")
        return redirect(  'home')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj': room, 'title': title})


@login_required(login_url='login')
def deleteMessage(request, pk):
    title = "Delete a message"
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        messages.error(request, "Apologies! you cannot delete this message.")
        return redirect(  'room' , pk=room.id)
    if request.method == 'POST':
        message.delete()
        messages.error(request, " you've deleted the message.")
      
        return redirect('room', pk=message.room.id)
    return render(request, 'base/delete.html',{'obj': message, 'title': title})

@login_required(login_url='login')
def updateUser(request):
    title = "Update your profile"
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES ,instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html',{'form':form, 'title': title})



def topicsPage(request):
    title = "Topics page"
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics, 'title': title})


def activityPage(request):
    title = "Activities"
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages, 'title': title})