from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import permissions, generics,status
from django.contrib.auth import get_user_model
from notifications.signals import notify
from .models import saladeChat,participantesChat,mensajeEnChat
from .serializers import UsuarioSerializer,salaChatSerializer,parcipantesSerializer,mensajEnSalaDeChat

# Create your views here.


class UserCreate(APIView):
  permission_classes = (AllowAny,)
  def post(self, request, format='json'):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      if user:
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
        return Response("user not saved")
    else:
      return Response(serializer.errors)

class salaDeChatView1(APIView):
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
    
    notif_args = {
      'source': user,
      'source_display_name': user.get_full_name(),
      'category': 'chat', 'action': 'Sent',
      'obj': chat_session_message.id,
      'short_description': 'You a new message', 'silent': True,
      'extra_data': {'uri': chat_session.uri}
      }
    notify.send(sender=self.__class__, **notif_args, channels=['websocket'])

    return Response({
      'mensaje': mensaje
    })



    