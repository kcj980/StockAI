from django.shortcuts import render, redirect

# ViewSets
from rest_framework import viewsets, permissions, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Message, Comment
from .serializers import MessageSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer

class CustomPagination(PageNumberPagination):
  page_size = 5
  page_size_query_param = 'page_size'
  max_page_size = 1000

  def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page': self.page.number,
            'page_obj': self.page,
            'total': range(1, self.page.paginator.num_pages + 1),
            'messages': data['messages']
        }, template_name=data['template'])

class MessageViewSet(viewsets.ModelViewSet):
  serializer_class = MessageSerializer
  queryset = Message.objects.all()
  renderer_classes = [TemplateHTMLRenderer]
  pagination_class = CustomPagination
  permission_classes = [IsOwnerOrReadOnly]
  # template_name = 'board/message.html'

  def list(self, request, *args, **kwargs):
    queryset = Message.objects.all().order_by('-pk')

    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        data = {'messages':serializer.data, 'template': 'board/list.html'}
        return self.get_paginated_response(data=data)
        # return self.get_paginated_response(data=serializer.data, template_name='board/list.html')

    serializer = self.get_serializer(queryset, many=True)
    return Response(data={'messages': serializer.data}, template_name='board/list.html')
  
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    obj = self.perform_create(serializer)
    pk = obj.pk
    
    return redirect(reverse('board:message-detail', args=[pk]))

  def perform_create(self, serializer):
    return serializer.save(user=self.request.user)
  
  def get(self, request, *args, **kwargs):
    serializer = MessageSerializer()
    return render(request, template_name='board/new.html', context={'serializer':serializer.data})

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    message_id = self.kwargs['pk']
    comment = Comment.objects.filter(message=instance)
    comments = CommentSerializer(comment, many=True)
    request_user = request.user
    print(comments.data)
    
    return Response(data={'message': serializer.data, 'comments':comments.data, 'pk':self.kwargs['pk'], 'requset_user':request_user}, template_name='board/detail.html')
  
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return redirect(reverse('board:message-list'))
    # return redirect('/board/list')


  def get_update(self, request, *args, **kwargs):
    # print(self.get_serializer(self.get_object()).data)
    # serializer = MessageSerializer()
    serializer = self.get_serializer(self.get_object())

    return render(request, template_name='board/edit.html', context={'message':serializer.data})


  def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    pk = self.kwargs['pk']

    if getattr(instance, '_prefetched_objects_cache', None):
        # If 'prefetch_related' has been applied to a queryset, we need to
        # forcibly invalidate the prefetch cache on the instance.
        instance._prefetched_objects_cache = {}

    return redirect(reverse('board:message-detail', args=[pk]))

class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  renderer_classes = [TemplateHTMLRenderer]
  # template_name = 'board/comments.html'
  pagination_class = CustomPagination
  permission_classes = [IsOwnerOrReadOnly]
  

  def get_queryset(self):
    # message=self.kwargs['message_id']
    message=self.kwargs.get('message_id')
    Message.objects.filter()
    return self.queryset.filter(message=message)

  def list(self, request, *args, **kwargs):
    message_id = self.kwargs['pk']
    message = Message.objects.get(pk=message_id)

    # queryset = Comment.objects.all().order_by('-pk')
    # comments = message.comment_set.all()
    comments = Comment.objects.filter(message=message)

    page = self.paginate_queryset(comments)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        data = {'data':serializer.data, 'template': 'board/comments.html'}
        return self.get_paginated_response(data=data)
        # return self.get_paginated_response(data=serializer.data, template_name='board/list.html')

    serializer = self.get_serializer(comments, many=True)
    # print(serializer.data)
    return Response(data={'data': serializer.data, 'pk':self.kwargs['pk'] }, template_name='board/comments.html')

  
  def create(self, request, *args, **kwargs):
    message_id = self.kwargs['pk']
    # print(self.get_serializer(data=request.data))
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=self.request.user, message_id = message_id)
    
    return redirect(reverse('board:message-detail', args=[message_id]))

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return redirect('board:message-detail', pk=self.kwargs['message_id'])

  # def destroy(self, request, *args, **kwargs):
  #   instance = self.get_object()
  #   self.perform_destroy(instance)
  #   return redirect(reverse('board:message-list'))