from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# app_name = 'stock'

urlpatterns = [
    path('list/', views.StockListViewSet.as_view({'get':'list'}), name='list'),
    path('ranking/', views.StockRankingView.as_view(), name='ranking'),
    path('userstock/', views.UserstockListViewSet.as_view({'get':'list'}), name='userstock'),
    path('userstock/buy/', views.UserstockBuyingViewSet.as_view({'get':'list','post':'create_or_update'}), name='userstock-buy'),
    path('userstock/sell/', views.UserstockSellingViewSet.as_view({'get':'list','post':'delete_or_update'}), name='userstock-sell'),
    path('userstock/buy/api/', views.UserStockBuyingAPI.as_view({'get':'list','post':'create'}), name='userstock-buy-api'),
    path('userstock/buy/api/<int:pk>/', views.UserStockBuyingAPI.as_view({'get':'retrieve','put':'update', 'delete':'destroy'}), name='userstock-buy-api2'),
    path('', views.StockDataTamplate.as_view(), name='stock-list'),
    # path('detail/', views.StockDataDetailViewSet.as_view({'get':'list'}), name='stock-detail'),
    # path('', views.),
    # path('/', views.SnippetList.as_view()),
    # path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    # path('list/', views.list, name="list1"),
]
