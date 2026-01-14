from django.urls import path
from my_apps.blog.views import PostListView

app_name = 'blog'

urlpatterns = [
    path('', PostListView, name='post_list'),
]