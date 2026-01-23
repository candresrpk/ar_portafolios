from django.urls import path
from my_apps.usuarios import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.registerView, name='signup'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('profile/', views.profileView, name='profile'),
]