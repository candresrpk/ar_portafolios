from django.urls import path
from my_apps.blog.views import PostListView, create_post_view

app_name = 'blog'

urlpatterns = [
    path('', PostListView, name='post_list'),
    path('create/', create_post_view, name='create_post'),
]