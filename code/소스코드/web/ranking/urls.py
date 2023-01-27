from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.UserRankingMain.as_view(), name='ranking-list'),
    # path('api/', views.UserRankingAPI.as_view({'get':'list'}), name='ranking-api'),
]