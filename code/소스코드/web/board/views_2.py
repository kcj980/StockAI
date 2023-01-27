from django.shortcuts import render, redirect, get_object_or_404
from board.models import Message, Comment
from board.serializers import MessageSerializer, CommentSerializer

from board.forms import MessageForm, CommentForm
from django.views.decorators.http import require_POST
from rest_framework import viewsets
# Create your views here.

class MessageViewSet(viewsets.ModelViewSet):
  queryset = Message.objects.all()
  serializer_class = MessageSerializer
class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer

def message_list(request):
    messages = Message.objects.all()
    return render(request, 'board/list.html', {'messages': messages})

def message_detail(request, pk):
    message = Message.objects.get(pk=pk)
    return render(request, 'board/detail.html', {'message': message})

def message_new(request):
    if request.user.is_authenticated:
      if request.method == "POST":
          print("-------------------------")
          print(dir(request))
          print("-------------------------")
          form = MessageForm(request.POST)
          
          if form.is_valid():
          # message.user = request.user
            message = form.save(commit=False)

            message.save()
            return redirect('detail', pk=message.pk)
      else:
          form = MessageForm()
      return render(request, 'board/new.html')
    else:
      return redirect('accounts:login')

def message_edit(request, pk):
  if request.user.is_authenticated:
    message = Message.objects.get(pk=pk)
    
    if request.user == message.user:
      if request.method == "POST":
          form = MessageForm(request.POST, instance=message)
          if form.is_valid():

              message = form.save(commit=False)
              message.save()
              return redirect('detail', pk=message.pk)
      else:
          form = MessageForm(instance=message)
      return render(request, 'board/edit.html', {'form': form})
    else:
      return redirect('warning')
  else:
    return redirect('accounts:login')

def message_delete(request, pk):
    message = Message.objects.get(pk=pk)
    if message.user == request.user.get_username():
      message.delete()
    else:
      return redirect('warning')
    return redirect('list')

@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        message = get_object_or_404(Message, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.message = message
            comment.user = request.user
            comment.save()
        return redirect('detail', message.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, message_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('detail', message_pk)
