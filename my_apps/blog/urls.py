from django.urls import path
from my_apps.blog.views import PostListView, createPostView, postDetailView, createEntryView

app_name = 'blog'

urlpatterns = [
    path('', PostListView, name='post_list'),
    path('create/', createPostView, name='create_post'),
    path('post/<slug:slug>/', postDetailView, name='post_detail'),
    path('post/<int:id>/entry/create/', createEntryView, name='add_entry'),
]