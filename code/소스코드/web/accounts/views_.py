from django.shortcuts import render, redirect
from django.urls import reverse

from rest_framework import generics, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

# from accounts.models import Userdata
from accounts.serializers import UserSerializer

# Create your views here.
class CreateUser(generics.CreateAPIView):
  renderer_classes = [TemplateHTMLRenderer]
  template_name = "registration/signup.html"

  serializer_class = UserSerializer
  permission_classes = [
      permissions.AllowAny
  ]
  # queryset = User.objects.all()

  def get(self, request):
    serializer = UserSerializer()
    return Response({'serializer': serializer})

  def post(self, request, *args, **kwargs):
    serializer = UserSerializer(data=request.data)
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']
    if password != password_confirm:
      return render(request, 'signup', {'message':'Password not match.'})
    super().post(request, *args, **kwargs)
    return redirect(reverse('login'))
