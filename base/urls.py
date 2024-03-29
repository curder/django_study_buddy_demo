from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.index, name='index'),
    path('rooms/<str:pk>/destroy/', views.destroyRoom, name='rooms.destroy'),
    path('rooms/<str:pk>/update/', views.updateRoom, name='rooms.update'),
    path('rooms/create/', views.createRoom, name='rooms.create'),
    path('rooms/<str:pk>', views.room, name='rooms.show'),
    path('profile/update/', views.updateProfile, name='profile.update'),
    path('profile/<str:pk>/', views.profile, name='profile.show'),
    path('messages/<str:pk>/destroy', views.destroyMessage, name='messages.destroy'),
    path('topics/', views.topics, name='topics.index'),
    path('activities/', views.activities, name='activities.index'),
]
