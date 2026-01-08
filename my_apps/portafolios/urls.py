from django.urls import path
from . import views

app_name = 'portafolios'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('projects/', views.ProjectsView, name='projects'),
    path('create/', views.CreateProjectView, name='create'),
    path('project/<int:id>/', views.ProjectDetailView, name='detail'),
    path("under-construction/", views.under_construction, name="under_construction"),
]