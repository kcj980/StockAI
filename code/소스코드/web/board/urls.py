from django.urls import path, include
from board import views
from rest_framework.routers import DefaultRouter


app_name = 'board'

router = DefaultRouter()
router.register(r'message', views.MessageViewSet, basename='board')
router.register(r'comment', views.CommentViewSet, basename='comment') # (댓글)


message_list = views.MessageViewSet.as_view({'get':'list'})
# message_list = views.MessageListViewSet.as_view({'get':'list'})
message_detail = views.MessageViewSet.as_view({'get': 'retrieve'})
message_create = views.MessageViewSet.as_view({'get': 'get', 'post': 'create'})
message_delete = views.MessageViewSet.as_view({'post': 'destroy'})
message_update = views.MessageViewSet.as_view({'get':'get_update', 'post': 'update'})
# message_delete = views.MessageDeleteViewSet.as_view({'delete': 'destroy'})

# comment_list = views.CommentViewSet.as_view({'get':'list'})
# comment_create = views.MessageViewSet.as_view({'post': 'create'})
# comment_delete = views.MessageViewSet.as_view({'post': 'delete'})
comments = views.CommentViewSet.as_view({'post': 'create', 'get':'list'})
comment_delete = views.CommentViewSet.as_view({'post': 'destroy'})

urlpatterns = [
  path('', include(router.urls)),
  path('new/', message_create, name='message-create'),
  path('list/', message_list, name='message-list'),
  # path('detail/<int:pk>/delete/', message_delete, name='message-delete'),
  path('detail/<int:pk>', message_detail, name='message-detail'),
  path('delete/<int:pk>', message_delete, name='message-delete'),
  path('update/<int:pk>', message_update, name='message-update'),
  path('detail/<int:pk>/comments', comments, name='comments'),
  # path('detail/<int:message_id>/comments/<int:comment_id>/delete', comment_delete, name='comment-delete'),
  path('detail/<int:message_id>/comments/<int:pk>/delete', comment_delete, name='comment-delete'),
  # path('comments/<int:pk>', message_update, name='message-update'),
  # path('detail/<int:pk>/update', message_update, name='message-detail'),
  # path('detail/<int:pk>/comments', comments, name='comments')
  # path('message/list', views.M)
]

# urlpatterns = [
#   path('', views.message_list, name='list'),
#   path('new/', views.message_new, name='new'),
#   path('edit/', views.message_edit, name='edit'),
#   path('detail/<int:pk>', views.message_edit, name='detail'),
#   path('delete/', views.message_delete, name='delete'),
#   path('<int:pk>/comments/', views.message_list, name='comment_new'),
#   path('<int:message_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comment_delete'),
# ]