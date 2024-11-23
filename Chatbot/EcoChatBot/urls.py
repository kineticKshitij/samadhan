from django.urls import path
from EcoChatBot import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat-response/', views.ChatResponse, name='chat-response'),
]
