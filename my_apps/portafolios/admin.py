from django.contrib import admin
from my_apps.portafolios.models import Project, Tag

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