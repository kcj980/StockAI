from collections import OrderedDict
import requests
import json

from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django.db.models import Q

from django.shortcuts import render

from accounts.models import *
from ranking.serializers import UserRankingSerializer
from .serializers import *

# Create your views here.
class MacroListViewSet(viewsets.ModelViewSet):
    queryset = Macroeconomicindicators.objects.all().order_by('-date_time')
    serializer_class = MacroSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    

class MacroMain(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'macro/list.html'
    permission_classes = [
        permissions.AllowAny
    ]
    def get(self, request):
        url_macro = 'http://127.0.0.1:8000/macro/api/'
        response_macro = requests.get(url_macro)
        macro_list = response_macro.json()['results'][:14]
        
        choice = request.GET.get('choice','')
        if choice == '':
            choice = 'kospi'
            color = '#2E8B57'
            
        if choice == 'kospi':
            title = 'KOSPI'
            color = '#2E8B57'
        elif choice == 'america_top_500':
            title = '미국 상위 500 주식'
            color = '#008080'
        elif choice == 'gold':
            title = '금'
            color = '#3CB371'
        elif choice == 'copper':
            title = '구리'
            color = '#90EE90'
        elif choice == 'k_gov3':
            title = '3년 한국채 수익률'
            color = '#4FAFAF'
        elif choice == 'usd_k':
            title = '환율'
            color = '#6FAF3F'
                    
        return Response({'macro_list':macro_list, 'title':title, 'choice':choice, 'color':color})