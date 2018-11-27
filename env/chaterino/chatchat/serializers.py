from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import saladeChat, mensajeEnChat, participantesChat

class UsuarioSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset = User.objects.all())])
  username = serializers.CharField(validators = [UniqueValidator(queryset = User.objects.all())])
  password = serializers.CharField(write_only = True)

  def create(self, validated_data):
    user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
    return user

    class Meta:
      model = User
      fields = ('username','email','password')
  

class salaChatSerializer(serializers.ModelSerializer):

    class Meta:
      model = saladeChat
      fields ='__all__'

class parcipantesSerializer(serializers.ModelSerializer):
  class Meta:
    model = participantesChat
    fields = '__all__'

class mensajEnSalaDeChat(serializers.ModelSerializer):
  class Meta:
    model = mensajeEnChat
    fields = '__all__'

  

  