from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4


User = get_user_model()


class rastreador(models.Model):
  fecha_creacion = models.DateTimeField(auto_now_add = True)
  fecha_update = models.DateTimeField(auto_now = True)

  class Meta:
    abstract = True

def generar_uri():
  return str(uuid4()).replace('-','')[:15]


class saladeChat(rastreador):
  dueno = models.ForeignKey(User,on_delete = models.PROTECT)
  uri = models.URLField(default = generar_uri)
  topico = models.CharField(max_length  = 100)

class mensajeEnChat(rastreador):
  user = models.ForeignKey(User, on_delete= models.PROTECT)
  sala_chat = models.ForeignKey(saladeChat,related_name = 'mensajes', on_delete= models.PROTECT)
  mensaje = models.TextField(max_length = 1000)
  

class participantesChat(rastreador):
  sala_chat = models.ForeignKey(saladeChat,related_name = 'participantes', on_delete = models.PROTECT)
  user = models.ForeignKey(User, on_delete = models.PROTECT)

# Create your models here.
