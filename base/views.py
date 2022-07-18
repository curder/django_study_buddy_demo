from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm


# rooms = [
#     {"id": 1, "name": "Let's learn Python!"},
#     {"id": 2, "name": "Design with me"},
#     {"id": 3, "name": "Frontend developers"},
# ]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)
    topics = Topic.objects.all()  # 获取所有表数据
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context=context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {"room": room}

    return render(request, 'base/room.html', context=context)


def createRoom(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    form = RoomForm()
    context = {'form': form}
    return render(request, 'base/room_form.html', context=context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
        return redirect('home')

    context = {"form": form}

    return render(request, 'base/room_form.html', context=context)


def destroyRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {"obj": room}
    return render(request, 'base/destroy.html', context=context)
