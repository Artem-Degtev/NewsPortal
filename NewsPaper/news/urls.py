from django.contrib import admin
from django.urls import path, include
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, subscriptions

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_add'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]