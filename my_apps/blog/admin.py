from django.contrib import admin
from my_apps.blog.models import Post, Tag, PostContent
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'author__username']
    list_filter = ['created_at']
    list_per_page = 10
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    list_per_page = 10
    
    
@admin.register(PostContent)
class PostContentAdmin(admin.ModelAdmin):
    list_display = ['post', 'content']
    search_fields = ['post__title', 'content']
    list_per_page = 10
