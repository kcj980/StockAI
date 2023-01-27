from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.MacroMain.as_view(), name='macro-main'),
    path('api/', views.MacroListViewSet.as_view({'get':'list'}), name='macro-api'),
]