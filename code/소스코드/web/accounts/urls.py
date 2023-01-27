from django.urls import path, include
from accounts.views import UserViewSet, SignupViewSet, DeleteViewSet, ProfileViewSet
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

app_name = 'accounts'

router = DefaultRouter()
# router.register(r'accounts', UserViewSet)

profile = ProfileViewSet.as_view({'get':'get_update','post':'update'}, name='profile-update')
signup = SignupViewSet.as_view({'post':'create'}, name='signup')
delete = DeleteViewSet.as_view({'get':'get','post':'destroy'}, name='delete')

urlpatterns = [
  path('', include(router.urls)),
  # path('signup/', UserViewSet.as_view({'get': 'get', 'post': 'create'}), name='signup'),
  path('signup/', signup, name='signup'),
  # path('profile/<str:userid>/', profile, name='profile'),
  path('profile/', profile, name='profile'),
  path('accounts/delete/<str:pk>', delete, name='delete')
  
  # path('login/', auth_views.LoginView.as_view(), name='login'),
  # path('logout/', auth_views.LogoutView.as_view(), name='logout')
]