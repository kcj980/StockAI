from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
app_name = 'ai'

urlpatterns = [
    path('', views.AIMain.as_view(), name='ai-main'),
    path('api/', views.AIrateListViewSet.as_view({'get':'list'}), name='ai-api'),
]