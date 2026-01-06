from django.shortcuts import render

# Create your views here.

def homeView(request):
    return render(request, './home.html')


def ProjectsView(request):
    return render(request, './portafolios/projects.html')