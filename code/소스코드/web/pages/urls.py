from django.urls import path
from pages import views

urlpatterns = [
    path('index/', views.index, name='home'),
    path('mypage/', views.mypage, name='mypage'),
    path('welcome/', views.welcome, name='welcome'),
]