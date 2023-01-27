from collections import OrderedDict
import requests
import json

from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django.db.models import Q
from django.shortcuts import render

from accounts.models import *
from .serializers import *

class DictListViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictSerializer
    filter_backends = [SearchFilter]
    search_fields = ('title',)
    permission_classes = [
        permissions.AllowAny
    ]

class DictPagination(PageNumberPagination):
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
            'dict_all': data['dict_all']
        }, template_name=data['template'])

class DictMainView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dict2.html'
    permission_classes = [permissions.AllowAny]
    pagination_class = DictPagination
    serializer_class = DictSerializer
    
    def get(self, request):
        queryset = Dictionary.objects.all()

        ### 검색 기능
        search_title = request.GET.get('title_name')
        if search_title != None:
            queryset = Dictionary.objects.filter(title__contains=search_title)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = {'dict_all':serializer.data, 'template': 'dict2.html'}
            return self.get_paginated_response(data=data)
        # return self.get_paginated_response(data=serializer.data, template_name='board/list.html')

        serializer = self.get_serializer(queryset, many=True)
        return Response(data={'dict_all': serializer.data}, template_name='dict2.html')


# Create your models here.
# class DictMainView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'dict2.html'
#     permission_classes = [permissions.AllowAny]
    
#     def get(self, request):
#         queryset = Dictionary.objects.all()
#         serializer = DictSerializer(queryset, many=True)
#         return Response({'dict_all':serializer.data})