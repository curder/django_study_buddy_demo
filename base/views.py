from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


# rooms = [
#     {"id": 1, "name": "Let's learn Python!"},
#     {"id": 2, "name": "Design with me"},
#     {"id": 3, "name": "Frontend developers"},
# ]

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exists.')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username or password does not exists')

    context = {}
    return render(request, 'base/auth/login.html', context=context)


def logoutPage(request):
    logout(request)
    return redirect('index')


def registerUser(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()  # 用户名转换为小写
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'An error occurred during register')

    form = MyUserCreationForm()
    context = {'form': form}
    return render(request, 'base/auth/register.html', context=context)


def index(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__contains=q) |
        Q(description__contains=q)
    )
    topics = Topic.objects.all()[:5]  # 获取前5条数据
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/index.html', context=context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created_at')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('rooms.show', pk=room.id)

    context = {"room": room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/rooms/show.html', context=context)


@login_required(login_url='/login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/auth/profile/show.html', context=context)


@login_required(login_url='/login')
def createRoom(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('index')

    form = RoomForm()
    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, 'base/rooms/form.html', context=context)


@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('index')

    topics = Topic.objects.all()
    context = {"form": form, 'topics': topics, 'room': room}
    return render(request, 'base/rooms/form.html', context=context)


@login_required(login_url='/login')
def destroyRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('index')

    context = {"obj": room}
    return render(request, 'base/destroy.html', context=context)


@login_required(login_url='/login')
def destroyMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('rooms.show', message.room.id)

    context = {"obj": message}
    return render(request, 'base/destroy.html', context=context)


@login_required(login_url='/login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # 用户名转换为小写
            user.save()
            return redirect('profile.show', user.id)

    context = {'form': form}
    return render(request, 'base/auth/profile/update.html', context=context)


def topics(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    topics = Topic.objects.filter(name__contains=q)

    context = {'topics': topics}
    return render(request, 'base/topics/index.html', context=context)


def activities(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}

    return render(request, 'base/activities/index.html', context=context)
