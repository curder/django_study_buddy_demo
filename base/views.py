from django.shortcuts import render

rooms = [
    {"id": 1, "name": "Let's learn Python!"},
    {"id": 2, "name": "Design with me"},
    {"id": 3, "name": "Frontend developers"},
]


def home(request):
    context = {'rooms': rooms}
    return render(request, 'home.html', context=context)


def room(request):
    return render(request, 'room.html')
