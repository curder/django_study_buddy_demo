from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.home, name='home'),
    path('rooms/<str:pk>/destroy/', views.destroyRoom, name='rooms.destroy'),
    path('rooms/<str:pk>/update/', views.updateRoom, name='rooms.update'),
    path('rooms/create/', views.createRoom, name='rooms.create'),
    path('rooms/<str:pk>', views.room, name='room'),
    path('profile/<str:pk>/', views.profile, name='profile.show'),
    path('messages/<str:pk>/destroy', views.destroyMessage, name='messages.destroy'),
]
