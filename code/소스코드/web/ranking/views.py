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

from accounts.models import *
from .serializers import *


class UserRankingMain(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'ranking/list.html'
    permission_classes = [
        permissions.AllowAny
    ]
    def get(self, request):
        queryset = Userdata.objects.all().order_by('-invest_value')
        serializer = UserRankingSerializer(queryset, many=True)
        userdata_json = json.loads(json.dumps(serializer.data))
        # print(userdata_json)
        for i in range(len(userdata_json)):
            for_sum_price = Userstock.objects.filter(userid=userdata_json[i]['userid']).only('count','stock_mean_price')
            sum_price = 0
            for fsp in for_sum_price:
                # print(fsp.count, fsp.stock_mean_price)
                sum_price += fsp.count * fsp.stock_mean_price
            if sum_price == 0:
                userdata_json[i]['current_return'] = 0.0
            else:
                userdata_json[i]['current_return'] = float(str(userdata_json[i]['invest_value'] / sum_price * 100 - 100)[:6])

            
            userdata_json[i]['accumulated_return'] = float(str(userdata_json[i]['total_money'] / 100000000 * 100 - 100)[:6])
            userdata_json[i]['invest_div_total'] = float(str(userdata_json[i]['invest_value'] / userdata_json[i]['total_money'] * 100)[:6])
        
        sort = request.GET.get('sort','')
        if sort == '':
            sort = 'current_return'
        userdata_json = sorted(userdata_json, key=lambda x: x[f'{sort}'], reverse=True)
        # print(userdata_json)
        
        return Response({'rankings':userdata_json})
    

# ### test
# class UserRankingAPI(viewsets.ViewSet):
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     def list(self, request):
#         queryset = Userdata.objects.all().order_by('-invest_value')
#         serializer = UserRankingSerializer(queryset, many=True)
#         userdata_json = json.loads(json.dumps(serializer.data))
#         # print(userdata_json)
#         for i in range(len(userdata_json)):
#             for_sum_price = Userstock.objects.filter(userid=userdata_json[i]['userid']).only('count','stock_mean_price')
#             sum_price = 0
#             for fsp in for_sum_price:
#                 # print(fsp.count, fsp.stock_mean_price)
#                 sum_price += fsp.count * fsp.stock_mean_price
#             userdata_json[i]['current_return'] = str(userdata_json[i]['invest_value'] / sum_price * 100) + ' %'
#             sum_price = 0
            
#             userdata_json[i]['accumulated_return'] = str(userdata_json[i]['total_money'] / 100000000 * 100) + ' %'
#             userdata_json[i]['invest_div_total'] = str(userdata_json[i]['invest_value'] / userdata_json[i]['total_money'] * 100) + ' %'
        
#         sort = request.GET.get('sort','')
#         if sort == '':
#             sort = 'current_return'
#         userdata_json = sorted(userdata_json, key=lambda x: x[f'{sort}'], reverse=True)
        
#         return Response(userdata_json)
    