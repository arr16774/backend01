from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .models import saladeChat,participantesChat,mensajeEnChat
from .serializers import UsuarioSerializer,salaChatSerializer,parcipantesSerializer,mensajEnSalaDeChat

# Create your views here.
class salaDeChatView(APIView):
  permission_classes = (permissions.IsAuthenticated,)

  def post (self,request,*args, **kwargs):
    user = request.user
    topic = request.data['topico']
    sala_chat = saladeChat.objects.create(dueno = user, topico = topic)
    sala = salaChatSerializer(sala_chat)
    return Response ({
      'Status': sala.data
    })

  def patch(self, request, *args, **kwargs):
    User = get_user_model()
    uri = kwargs['uri']
    username = request.data['username']
    user = User.objects.get(username = username)
    sala_chat = saladeChat.objects.get(uri = uri)
    dueno = saladeChat.dueno

    if dueno != user:
      sala_chat.participantes.get_or_create(
        user = user, sala_chat = sala_chat
      )

    dueno = UsuarioSerializer(dueno)
    
    participantes = [
      UsuarioSerializer(sala_chat.user) for sala_chat in sala_chat.participantes.all()

    ]
    
    
    participantes.insert(0,dueno)
    

    return Response ({
      'status': user.username
      
    })

class salaDeChatView(APIView):
  permissions_classses = (permissions.IsAuthenticated,)

  def get(self, request, *args, **kwargs):
    uri = kwargs['uri']
    user = request.user
    sala_chat = saladeChat.objects.get(uri = uri)
    rekt = mensajeEnChat.objects.filter(sala_chat = sala_chat)
    sala2 = mensajEnSalaDeChat(rekt[1])
    sala1= salaChatSerializer(sala_chat)
    a = 0

    mensajes = [
     
    ]
  
    while a <  len(rekt):
      salalmao = mensajEnSalaDeChat(rekt[a])
      lmao = {
        'user': salalmao.data['user'],
        'mensaje': salalmao.data['mensaje']
      }
      mensajes.append(lmao)
      a += 1
    
    

    return Response({
      'id': sala_chat.id,
      'uri': sala_chat.uri,
      'holi': mensajes
    
    })

  def post(self,request,*args,**kwargs):
    uri = kwargs['uri']
    mensaje = request.data['mensaje']
    user = request.user
    sala_chat = saladeChat.objects.get(uri = uri)
    mensajeEnChat.objects.create(
      user = user, sala_chat = sala_chat, mensaje =mensaje

    )

    return Response({
      'mensaje': mensaje
    })



    