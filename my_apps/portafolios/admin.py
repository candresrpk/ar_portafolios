from django.contrib import admin
from my_apps.portafolios.models import Project, Tag, Entry, Comment, Like, View

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'author__username']
    list_filter = ['created_at']
    list_per_page = 10


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    list_per_page = 10
    
    
@admin.register(Entry)
class PorjectContentAdmin(admin.ModelAdmin):
    list_display = ['project', 'content']
    search_fields = ['project__title', 'content']
    list_per_page = 10
    
    
    
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(View)
