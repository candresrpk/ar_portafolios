from django.urls import path
from . import views

app_name = 'portafolios'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('about/', views.aboutView, name='about'),
    path('projects/', views.ProjectsView, name='projects'),
    path('create/', views.CreateProjectView, name='create'),
    path('project/<int:id>/', views.ProjectDetailView, name='detail'),
    path('comment/<int:id>/', views.add_comment_view, name='add_comment'),
    
    path('entry/create/<int:project_id>/', views.CreateEntryView, name='add_entry'),
    
    path("under-construction/", views.under_construction, name="under_construction"),
]