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
from stock.serializers import UserstockListSerializer

# Create your views here.
def index(request):
    ### 1. AI 모델 그래프 나타내는 부분 관련
    
    ### 2. 주식 현황 및 모의 투자 - 급등 주식 랭킹 나타내는 부분 관련 (완료)
    # url_ranking = 'http://127.0.0.1:8000/stock/ranking/'
    # response_ranking = requests.get(url_ranking)
    # stock_ranking = response_ranking.json()['results'][:5]
    ai_accuracy = Stockcode.objects.all().order_by('stock_code')
    last_time = Modelresult.objects.last().date_time
    ai_fluctuation = Modelresult.objects.filter(date_time=last_time).order_by('stock_code')
    ai_dict_list = []
    for i,j in zip(ai_accuracy, ai_fluctuation):
        ai_dict = dict()
        ai_dict['stock_code'] = i.stock_code
        ai_dict['stock_name'] = i.stock_name
        ai_dict['total_score'] = int((i.xgb_short_pred + i.ltms_short_pred + j.xgb_short_result + j.lstm_short_result) / 4 * 10000) /100
        ai_dict_list.append(ai_dict)
    ai_dict_list = sorted(ai_dict_list, key= lambda x: x['total_score'], reverse=True)[:5]
    
    # ### 3. 코스피 나타내는 부분 관련 (완료)
    # url_macro = 'http://127.0.0.1:8000/macro/api/'
    # response_macro = requests.get(url_macro)
    # macro_data = response_macro.json()['results']
    
    ### 4. 모의투자 랭킹 나타내는 부분 관련 (완료)
    queryset = Userdata.objects.all().order_by('-invest_value')
    serializer = UserRankingSerializer(queryset, many=True)
    userdata_json = json.loads(json.dumps(serializer.data))
    
    for i in range(len(userdata_json)):
        for_sum_price = Userstock.objects.filter(userid=userdata_json[i]['userid']).only('count','stock_mean_price')
        sum_price = 0
        for fsp in for_sum_price:
            sum_price += fsp.count * fsp.stock_mean_price
        if sum_price == 0:
            userdata_json[i]['current_return'] = 0.0
        else:
            userdata_json[i]['current_return'] = float(str(userdata_json[i]['invest_value'] / sum_price * 100 - 100)[:6])

    userdata_json = sorted(userdata_json, key=lambda x: x['current_return'], reverse=True)[:7]
    # print(userdata_json)
    
    last_time = str(last_time)
    last_time = last_time[:4] + '년 ' + last_time[5:7] + '월 ' + last_time[8:10] + '일'
    # print(last_time)
    
    return render(request, 'base2.html', {'stock_ranking_all':ai_dict_list, 'user_ranking_all':userdata_json, 'last_time':last_time})


# 마이페이지 현재 투자 정보
def mypage(request):
  user = request.user
  userstock = Userstock.objects.filter(userid = user)
  
  for_sum_price = Userstock.objects.filter(userid=user).only('count','stock_mean_price')
  sum_price = 0.0
  for fsp in for_sum_price:
    sum_price += fsp.count * fsp.stock_mean_price
  
  current_return = "0"
  if sum_price != 0:
    current_return = str((round((user.invest_value / sum_price)- 1, 3)))
  current_return += " %"
  
  result = {'username': user.user_name,
            'total_money': user.total_money,
            'now_money': user.now_money,
            'invest_value': user.invest_value,
            'total_cnt': 0,
            'current_return': current_return,
           }
  stock_cnt = {}

  for data in userstock.values_list():
    stock_cnt[Stockcode.objects.filter(stock_code = data[2]).values_list()[0][1]] = data[3]*data[5]
    result['total_cnt'] += data[3]

  stock_labels = list(stock_cnt.keys())
  stock_values = list(stock_cnt.values())

  ############################
  serializer = UserstockListSerializer(userstock, many=True)
  userstock_json = json.loads(json.dumps(serializer.data))

  if not userstock_json:
      userstock_json_sub = []
  else:
      userstock_json_sub = userstock_json[0]
      for i in range(len(userstock_json)):
        userstock_json[i]['profit'] = userstock_json[i]['sum_stock_value'] - (userstock_json[i]['stock_mean_price'] * userstock_json[i]['count'])
  ############################

  context = {'user':user, 'result': result, 'labels': stock_labels, 'values':stock_values, 'userstock_all':userstock_json, 'userstock_sub':userstock_json_sub}
  return render(request, 'board/mypage.html', context=context)

def get_object(self):
  return self.request.user


def welcome(request):
    return render(request, 'main.html')