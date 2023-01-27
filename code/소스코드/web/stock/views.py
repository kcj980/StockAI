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

from accounts.models import Stockdata, Userstock, Stockcode
from .serializers import *


# class StockDataPageNumberPagination(PageNumberPagination):
#     page_size = 10
#     # page_size_query_param = 'page_size'
#     # max_page_size = 1000

#     def get_paginated_response(self, data):
#         return Response(OrderedDict([
#             ('StockDataList', data),
#             ('pageCnt', self.page.paginator.num_pages),
#             ('curPage', self.page.number),
#         ]))


# class StockDataListView(generics.ListAPIView):
#     queryset = Stockdata.objects.all()
#     serializer_class = StockdataSerializer
#     pagination_class = StockDataPageNumberPagination
    

# class StockDataDetailView(generics.RetrieveAPIView):
    
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)


# class StockDataPageNumberPagination(PageNumberPagination):
#     page_size = 10
#     # page_size_query_param = 'page_size'
#     # max_page_size = 1000

#     def get_paginated_response(self, data):
#         return Response(OrderedDict([
#             ('StockDataList', data),
#             ('pageCnt', self.page.paginator.num_pages),
#             ('curPage', self.page.number),
#         ]))
    

# ### 첫번째 방식
# class StockDataList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'stock/list.html'
    
#     def get(self, request):
#         stock_data = Stockdata.objects.all()
#         search_key = request.GET.get('stock_code')
#         if search_key:
#             stock_data = Stockdata.objects.filter(stock_code__icontains=search_key)
#         return Response({'stock_data_all': stock_data, 'q':search_key})


###
# 두번째 방식 : 주소를 통해 호출가능한 api 만들고 이를 활용
###

# 1) stockdata 필터링 조회
class StockListViewSet(viewsets.ModelViewSet):
    queryset = Stockdata.objects.all().order_by('-data_time')
    serializer_class = StockListSerializer
    # pagination_class = StockDataPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ('stock_code__stock_code',)
    permission_classes = [
        permissions.AllowAny
    ]

# 2) stockdata 가장 최근 날짜 등락률 탑 20 조회
class StockRankingView(generics.ListAPIView):
    last_time = Stockdata.objects.last().data_time
    queryset = Stockdata.objects.filter(data_time__gte=last_time).select_related().order_by('-end_rate_change')[:20]
    # queryset = queryset.only('id','stock_code', 'end_close', 'end_rate_change','stock_code__stock_name')
    serializer_class = StockRankingSerializer
    permission_classes = [
        permissions.AllowAny
    ]

# 3) userstock 조회
class UserstockListViewSet(viewsets.ViewSet):
    permission_classes = [
        permissions.AllowAny
    ]
    def list(self, request):
        queryset = Userstock.objects.filter(userid=request.user)
        serializer = UserstockListSerializer(queryset, many=True)
        return Response(serializer.data)

# 4) userstock 매수&매도 api
class UserStockBuyingAPI(viewsets.ModelViewSet):
    queryset = Userstock.objects.all()
    serializer_class = UserstockCreateSerializer
    permission_classes = [
        permissions.AllowAny
    ]

# 5) userstock 매수 : 탬플릿 + 메인
class UserstockBuyingViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'stock/buying.html'
    permission_classes = [
        permissions.AllowAny
    ]
    def list(self, request):
        return Response()
    def create_or_update(self, request):
        data = request.data
        last_time = Stockdata.objects.last().data_time
        buy_stock_name = data['stock_name']
        buy_count = int(data['count'])
        buy_stock_code = Stockcode.objects.get(stock_name=buy_stock_name).stock_code
        buy_price = Stockdata.objects.get(Q(stock_code=buy_stock_code) & Q(data_time=last_time)).end_close
        sum_price = buy_count * buy_price
        
        if Userdata.objects.get(userid=request.user).now_money < sum_price: # 0) 돈이 부족한 경우
            print('돈이 부족합니다.')
            return Response()
        
        matching_stock_code = Userstock.objects.filter(Q(userid=request.user) & Q(stock_code=buy_stock_code))
        if matching_stock_code: # 1) 이미 해당 주식 보유한 경우 : update
            pk = int(matching_stock_code[0].id)
            old_buy_count = matching_stock_code[0].count
            old_price = matching_stock_code[0].stock_mean_price
            mean_price = (old_price*old_buy_count + buy_price*buy_count) // (old_buy_count+buy_count)
            d = {
                'userid': request.user,
                'stock_code': buy_stock_code,
                'count': old_buy_count+buy_count,
                'stock_mean_price': mean_price,
                'stock_value': buy_price,
                'sum_stock_value': (old_buy_count+buy_count)*buy_price
            }
            data2 = requests.put(f'http://127.0.0.1:8000/stock/userstock/buy/api/{pk}/', data=d)
            print(data2)
            print('수정완료')
            
        else: # 2) 해당 주식 보유 X 경우 : create
            d = {
                'userid': request.user,
                'stock_code': buy_stock_code,
                'count': buy_count,
                'stock_mean_price': buy_price,
                'stock_value': buy_price,
                'sum_stock_value': buy_count*buy_price
            }
            print(d)
            data2 = requests.post('http://127.0.0.1:8000/stock/userstock/buy/api/', data=d)
            print(str(data2))
            print('생성완료')
        
        if str(data2) in ['<Response [200]>', '<Response [201]>']:
            a_user = Userdata.objects.get(userid=request.user)
            a_user.now_money = a_user.now_money - sum_price
            a_user.invest_value = a_user.invest_value + sum_price
            a_user.save()
            print('saved.')
        
        return Response()

# 6) userstock 매도 : 탬플릿 + 메인
class UserstockSellingViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'stock/selling.html'
    permission_classes = [
        permissions.AllowAny
    ]
    def list(self, request):
        return Response()
    def delete_or_update(self, request):
        data = request.data
        last_time = Stockdata.objects.last().data_time
        sell_stock_name = data['stock_name']
        sell_count = int(data['count'])
        sell_stock_code = Stockcode.objects.get(stock_name=sell_stock_name).stock_code
        sell_price = Stockdata.objects.get(Q(stock_code=sell_stock_code) & Q(data_time=last_time)).end_close
        sum_price = sell_count * sell_price
        
        matching_stock_code = Userstock.objects.filter(Q(userid=request.user) & Q(stock_code=sell_stock_code))
        if matching_stock_code[0].count > sell_count: # 1) 해당 종목의 일부만 판매하는 경우 : update
            pk = int(matching_stock_code[0].id)
            rest_count = matching_stock_code[0].count - sell_count
            old_price = matching_stock_code[0].stock_mean_price
            d = {
                'userid': request.user,
                'stock_code': sell_stock_code,
                'count': rest_count,
                'stock_mean_price': old_price,
                'stock_value': sell_price,
                'sum_stock_value': rest_count*sell_price
            }
            data2 = requests.put(f'http://127.0.0.1:8000/stock/userstock/buy/api/{pk}/', data=d)
            print(data2)
            print('수정완료')
            
        elif matching_stock_code[0].count == sell_count: # 2) 해당 종목 주식 다 판매하는 경우 : delete
            pk = int(matching_stock_code[0].id)
            data2 = requests.delete(f'http://127.0.0.1:8000/stock/userstock/buy/api/{pk}/')
            print(data2)
            print('삭제완료')
        
        else: # 3) 불가능한 경우 (ex. 가지고 있는 것보다 많은 것을 판매)
            print('불가능합니다.')
            return Response()
        
        if str(data2) in ['<Response [200]>', '<Response [204]>']:
            a_user = Userdata.objects.get(userid=request.user)
            a_user.now_money = a_user.now_money + sum_price
            a_user.invest_value = a_user.invest_value - sum_price
            a_user.save()
            print('saved.')
        
        return Response()

# 6) 메인 (다른 기능을 합쳐서 만듬)
class StockDataTamplate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'stock/list4.html'
    permission_classes = [
        permissions.AllowAny
    ]
    def get(self, request):
        ### 4-1) 등락률 top20 데이터 생성
        url_ranking = 'http://127.0.0.1:8000/stock/ranking/'
        response_ranking = requests.get(url_ranking)
        stock_ranking = response_ranking.json()['results'][:10]
        
        ### 4-2) AI 추천 종목 생성 : 모델 신뢰도 + 오를 가능성
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
        ai_dict_list = sorted(ai_dict_list, key= lambda x: x['total_score'], reverse=True)[:10]
        # print(ai_dict_list[:5])
        
        ### 4-3) 종목 검색 및 조회 + 그래프 생성을 위한 데이터 및 url 생성
        search_name = request.GET.get('stock_name')
        if search_name == None:
            search_name = 'KT'
        search_name = search_name.upper()
        search_code = Stockcode.objects.get(stock_name=search_name).stock_code
        url_list = f'http://127.0.0.1:8000/stock/list/?search={search_code}&format=json'
        response_list = requests.get(url_list)
        stock_list = response_list.json()['results'][:7]
        
        ai_result = Modelresult.objects.get(Q(stock_code=search_code) & Q(date_time=last_time))
        short_result = ai_result.xgb_short_result + ai_result.lstm_short_result
        long_result = ai_result.xgb_long_result + ai_result.lstm_long_result
        if short_result >= 1.5:
            short_suggest = '매수 추천'
        elif short_result < 0.5:
            short_suggest = '매도 추천'
        else:
            short_suggest = '중립'
        if long_result >= 1.5:
            long_suggest = '매수 추천'
        elif long_result < 0.5:
            long_suggest = '매도 추천'
        else:
            long_suggest = '중립'
        
        ### 4-4) user의 모의투자정보 조회
        # url_userstock = 'http://127.0.0.1:8000/stock/userstock/'
        # response_userstock = requests.get(url_userstock)
        queryset = Userstock.objects.filter(userid=request.user)
        serializer = UserstockListSerializer(queryset, many=True)
        userstock_json = json.loads(json.dumps(serializer.data))
        if not userstock_json:
            userstock_json_sub = []
        else:
            userstock_json_sub = userstock_json[0]
            for i in range(len(userstock_json)):
                userstock_json[i]['profit'] = userstock_json[i]['sum_stock_value'] - (userstock_json[i]['stock_mean_price'] * userstock_json[i]['count'])
                
        last_time = str(last_time)
        last_time = last_time[:4] + '년 ' + last_time[5:7] + '월 ' + last_time[8:10] + '일'
                
        return Response({'stock_ranking_all':stock_ranking, 'ai_dict_list':ai_dict_list, 'q_name': search_name, 'q':search_code, 'short_suggest':short_suggest, 'long_suggest':long_suggest, 'stock_list_all': stock_list, 'userstock_all':userstock_json, 'userstock_sub':userstock_json_sub, 'last_time':last_time})
