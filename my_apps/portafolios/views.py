from django.shortcuts import render, redirect, get_object_or_404
from my_apps.portafolios.models import Project, Tag, View
from my_apps.portafolios.forms import CreateProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from my_apps.portafolios.utils import get_client_ip

# Create your views here.
def homeView(request):
    return render(request, './home.html')

def ProjectsView(request):
    
    tag_slug = request.GET.get('tag')

    top_projects = Project.objects.filter(top=True)

    if tag_slug:
        projects = Project.objects.filter(tags__slug=tag_slug)
    else:
        projects = Project.objects.all()

    tags = Tag.objects.all()

    context = {
        'top_projects': top_projects,
        'projects': projects,
        'tags': tags,
        'active_tag': tag_slug,
    }

    return render(request, 'portafolios/projects.html', context)


def ProjectDetailView(request, id):
    project = get_object_or_404(Project, id=id)

    ip = get_client_ip(request)

    if request.user.is_authenticated:
        View.objects.get_or_create(
            project=project,
            user=request.user
        )
    else:
        if not View.objects.filter(
            project=project,
            ip_address=ip
        ).exists():
            View.objects.create(
                project=project,
                ip_address=ip
            )

    return render(request, 'portafolios/detail.html', {
        'project': project
    })



@login_required
def CreateProjectView(request):
    if not request.user.is_authenticated and request.user.is_staff :
        messages.error(
                request,
                '❌ Lo siento pero no tienes permisos para hacer esto ( ͡° ͜ʖ ͡°)'
            )
        return redirect('portafolios:projects')
    
    form = CreateProjectForm()
    
    if request.method == 'POST':
        form = CreateProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            form.save_m2m()  # importante por los tags (ManyToMany)
            messages.success(
                request,
                '✅ Proyecto creado correctamente.'
            )
            return redirect('portafolios:projects')
        else:
            messages.error(
                request,
                '❌ Hay errores en el formulario. Revisa los campos.'
            )
    else:
        form = CreateProjectForm()
    
    return render(request, './portafolios/create.html', {'form': form})



def custom_404_view(request, exception):
    return render(request, './extras/404.html', status=404)


def under_construction(request):
    """
    Vista para páginas que aún no están disponibles
    """
    return render(request, "./extras/under_construction.html", status=200)