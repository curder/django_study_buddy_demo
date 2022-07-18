from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/create', views.createRoom, name='rooms.create'),
    path('room/<str:pk>', views.room, name='room'),
]
