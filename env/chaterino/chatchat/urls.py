from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
  
    path('chats/', views.salaDeChatView1.as_view()),
    path('chats/users/create/',views.UserCreate.as_view()),
    path('chats/<uri>/', views.salaDeChatView.as_view()),
    path('chats/<uri>/mensajes/', views.salaDeChatView.as_view()),
]