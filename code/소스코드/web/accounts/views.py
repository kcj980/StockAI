from django.shortcuts import render, redirect
from accounts.models import Userdata
from accounts.serializers import UserSerializer, UserProfileSerializer
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
# Create your views here.

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import update_session_auth_hash

from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

class SignupViewSet(viewsets.ModelViewSet):
  serializer_class = UserSerializer
  renderer_classes = [TemplateHTMLRenderer]
  template_name = 'registration/signup.html'
  permission_classes = [
    AllowAny
  ]
  
  def get(self, request):
    serializer = UserSerializer()
    # serializer.is_valid(raise_exception=True)
    return Response({'serializer': serializer})

  def create(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    return HttpResponseRedirect(reverse('login'))

  # def perform_create(self, serializer):
  #   if ('password' in self.request.data):
  #     password = Userdata.make_password(self.request.data['password'])
  #     serializer.save(password=password)
  #   else:
  #     serializer.save()
  #   return super().perform_create(serializer)

class ProfileViewSet(viewsets.ModelViewSet):
  queryset = Userdata.objects.all()
  serializer_class = UserProfileSerializer
  
  renderer_classes = [TemplateHTMLRenderer]
  template_name = 'registration/profile.html'
  permission_classes = [
    IsAuthenticated
  ]

  # lookup_field = 'userid'

  def get(self, request, *args, **kwargs):
    userid = kwargs.get('userid')
    serializer = UserSerializer()
    # serializer.is_valid(raise_exception=True)
    return Response({'serializer': serializer})

  def get_update(self, request, *args, **kwargs):
    # serializer = MessageSerializer()
    serializer = self.get_serializer(self.get_object())
    return render(request, template_name='registration/profile.html', context={'serializer':serializer.data})

  def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)

    # if not instance.check_password(request.data.get("old_password")):
      

    try:
      serializer.is_valid(raise_exception=True)
    except serializers.ValidationError as e:
      return render(request, template_name='registration/profile.html', context={'serializer':serializer.data, 'error':e.detail})

    self.perform_update(serializer)

    password = request.data.get('new_password')
    if password:
      instance.set_password(password)
      instance.save()

    update_session_auth_hash(request, instance)

    return redirect(reverse('home'))

  def get_object(self):
    return self.request.user

  # def update(self, request, pk=None):
  #   user = self.get_object()
  #   serializer = self.get_serializer(user, data=request.data, partial=True)
  #   serializer.is_valid(raise_exception=True)
  #   # serializer.update(user, serializer.data)
  #   serializer.save()

  #   return Response(serializer.data)


  # def get_object(self):                         
  #   return self.request.user
  
  # def get_object(self):
  #   return self.user

class DeleteViewSet(viewsets.ModelViewSet):
  queryset = Userdata.objects.all()
  serializer_class = UserSerializer

  def get(self, request, *args, **kwargs):
    return render(request, template_name='registration/delete.html')

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return redirect(reverse('home'))

class UserViewSet(viewsets.ModelViewSet):
  queryset = Userdata.objects.all()
  serializer_class = UserSerializer
  renderer_classes = [TemplateHTMLRenderer]
  
  permission_classes = [AllowAny]

  def get(self, request, *args, **kwargs):
    queryset = Userdata.objects.all()
    return Response({'user': queryset}, template_name='signup.html')
  
  def create(self, request, *args, **kwargs):
    
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

  def partial_update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial = True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)
