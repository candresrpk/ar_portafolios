from django.urls import path
from my_apps.blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView, name='post_list'),
    path('create/', views.createPostView, name='create_post'),
    path('post/<slug:slug>/', views.postDetailView, name='post_detail'),
    path('post/<int:id>/delete/', views.deletePostView, name='delete_post'),
    path('post/<int:id>/edit/', views.editPostView, name='edit_post'),
    ## ENTRY URLS
    path('post/<int:id>/entry/create/', views.createEntryView, name='add_entry'),
    path('post/entry/<int:id>/edit/', views.editEntryView, name='edit_entry'),
    path('post/entry/<int:id>/delete/', views.deleteEntryView, name='delete_entry'),
]