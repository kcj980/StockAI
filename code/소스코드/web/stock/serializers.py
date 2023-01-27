from rest_framework.serializers import RelatedField, ModelSerializer, CharField, ReadOnlyField
from accounts.models import *


class StockListSerializer(ModelSerializer):
    class Meta:
        model = Stockdata
        fields = '__all__'
        

class StockRankingSerializer(ModelSerializer):
    # stock_code__stock_name = RelatedField(source='stockcode', read_only=True)
    # stock_code__stock_name = CharField(source='stock_code.stock_name')
    # stock_code__stock_name = ReadOnlyField(source='stockcode.stock_name')
    stock_name = CharField(source='stock_code.stock_name')
    
    class Meta:
        model = Stockdata
        fields = ['id','stock_code', 'end_close', 'end_rate_change', 'stock_name']
        
        
class StockCodeSerializer(ModelSerializer):
    class Meta:
        model = Stockcode
        fields = '__all__'
        
        
class UserstockListSerializer(ModelSerializer):
    user_name = CharField(source='userid.user_name')
    now_money = CharField(source='userid.now_money')
    invest_value = CharField(source='userid.invest_value')
    total_money = CharField(source='userid.total_money')
    stock_name = CharField(source='stock_code.stock_name')
    
    class Meta:
        model = Userstock
        fields = ['userid','user_name','now_money','invest_value','total_money','stock_name','count','stock_mean_price','stock_value','sum_stock_value']
        
        
class UserstockCreateSerializer(ModelSerializer):
    class Meta:
        model = Userstock
        fields = '__all__'
