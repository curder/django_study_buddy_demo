from django.shortcuts import render
from .models import Room


# rooms = [
#     {"id": 1, "name": "Let's learn Python!"},
#     {"id": 2, "name": "Design with me"},
#     {"id": 3, "name": "Frontend developers"},
# ]


def home(request):
    rooms = Room.objects.all()  # 获取所有表数据
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context=context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {"room": room}

    return render(request, 'base/room.html', context=context)
