from django.urls import path
from dict import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list/', views.DictListViewSet.as_view({'get':'list'}), name='dict-list'),
    path('', views.DictMainView.as_view(), name='dict'),
]
