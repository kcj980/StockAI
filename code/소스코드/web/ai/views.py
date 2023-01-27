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
from .serializers import *


# class AIrateListViewSet(viewsets.ModelViewSet):
#     queryset = Airate.objects.all().order_by('-date_time')
#     serializer_class = AIrateSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]


class AIrateListViewSet(viewsets.ViewSet):
    permission_classes = [
        permissions.AllowAny
    ]
    def list(self, request):
        queryset = Airate.objects.all().order_by('-date_time').only('date_time','synthesis_rate')
        serializer = AIrateSerializer(queryset, many=True)
        ai_profit_json = json.loads(json.dumps(serializer.data))
        
        for i,_ in enumerate(ai_profit_json):
            day_kospi = Macroeconomicindicators.objects.get(date_time=ai_profit_json[i]['date_time']).kospi
            ai_profit_json[i]['kospi'] = day_kospi
            ai_profit_json[i]['ai_profit'] = int(day_kospi * ai_profit_json[i]['synthesis_rate'] * 100) / 100
            
        return(Response({'ai_profit_json':ai_profit_json}))



# class AIMain(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'ai/list.html'
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     def get(self, request):


#       return Response()
class AIMain(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'ai/list.html'
    permission_classes = [
        permissions.AllowAny
    ]
    def get(self, request):
      top_stocks = Airate.objects.values().latest('date_time')
      top_stocks.pop('date_time')  
      top_stocks.pop('synthesis_rate')

      top_num = 12
      top_stocks = dict(sorted(top_stocks.items(), key=lambda item: item[1], reverse=True))
      top_codes = list(top_stocks.keys())[:top_num]
      top_labels = [list(Stockcode.objects.filter(stock_code = code).values())[0]['stock_name'] for code in top_codes]
      top_rates = list(map(lambda x:round((x-1)*100, 3), list(top_stocks.values())))[:top_num]
      #####################################

      max_num = 15
      # stock_codes = list(Aifunds.objects.values().latest('date_time').keys())[1:]
      stock_list = Aifunds.objects.values().latest('date_time')
      stock_list.pop('date_time')
      stock_list = dict(sorted(stock_list.items(), key=lambda item: item[1], reverse=True))

      stock_codes = list(stock_list.keys())[:max_num]

      labels = [list(Stockcode.objects.filter(stock_code = code).values())[0]['stock_name'] for code in stock_codes]
      values = list(stock_list.values())[:max_num]
      etc = sum(list(stock_list.values())[max_num:])
      labels += ['기타']
      values += [etc]

      ###########################################
      # [list(Airate.objects.filter(stock_code = code).values())[0]['stock_name'] for code in top_codes]
      latest_rates = Airate.objects.values().latest('date_time')
      latest_rates.pop('date_time')
      latest_rates.pop('synthesis_rate')

      rates = []
      for code in stock_codes:
        rates.append(latest_rates[code])

      # rates = list(map(lambda x:round(x-1, 3)*100, rates))
      rates = list(map(lambda x:round((x-1)*100, 3), rates))
      # rates = list(map(lambda x:round(x*100, 3), rates))
      display_list = zip(labels, values, rates)

      context = {'top_labels': top_labels, 'top_rates':top_rates, 'curr_labels': labels, 'curr_values':values, 'display':display_list}
      return Response(context)


def get_rates(request):
 
  top_stocks = Airate.objects.values().latest('date_time')
  top_stocks.pop('date_time')  
  top_stocks.pop('synthesis_rate')

  top_num = 10
  top_stocks = dict(sorted(top_stocks.items(), key=lambda item: item[1], reverse=True))
  top_codes = list(top_stocks.keys())[:top_num]
  top_labels = [list(Stockcode.objects.filter(stock_code = code).values())[0]['stock_name'] for code in top_codes]
  top_rates = list(map(lambda x:round(x-1, 3)*100, list(top_stocks.values())))[:top_num]
 
  context = {'top_labels': top_labels, 'top_rates':top_rates}
  return render(request, 'ai/rates-chart.html', context=context)

def get_funds(request):

  stock_codes = list(Aifunds.objects.values().latest('date_time').keys())[1:]
  labels = [list(Stockcode.objects.filter(stock_code = code).values())[0]['stock_name'] for code in stock_codes]
  values = list(Aifunds.objects.values().latest('date_time').values())[1:]
 
  print(len(values))
  context = {'curr_labels': labels, 'curr_values':values}
  return render(request, 'ai/funds-chart.html', context=context)