from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/destroy/', views.destroyRoom, name='rooms.destroy'),
    path('room/<str:pk>/update/', views.updateRoom, name='rooms.update'),
    path('room/create/', views.createRoom, name='rooms.create'),
    path('room/<str:pk>', views.room, name='room'),
]
