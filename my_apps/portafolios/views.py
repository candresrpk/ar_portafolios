from django.shortcuts import render, redirect, get_object_or_404
from my_apps.portafolios.models import Project, Tag, View, Comment
from my_apps.portafolios.forms import CreateProjectForm, CreateEntryForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from my_apps.portafolios.utils import get_client_ip



def custom_404_view(request, exception):
    return render(request, './extras/404.html', status=404)


def under_construction(request):
    """
    Vista para páginas que aún no están disponibles
    """
    return render(request, "./extras/under_construction.html", status=200)


# Create your views here.
def homeView(request):
    return render(request, './home.html')


def aboutView(request):
    return render(request, './about.html')


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
    entries = project.entries.all().order_by('order')
    comments = Comment.objects.filter(project=project).select_related('user')
    
    can_add_entry = (
        request.user.is_authenticated
        and request.user.is_staff
        and project.author == request.user
    )
    
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

    context = {
        'project': project,
        'entries': entries,
        'comments': comments,
        'can_add_entry': can_add_entry,
        'comment_form': CommentForm(),
    }
    
    return render(request, 'portafolios/detail.html', context)



@login_required
def CreateProjectView(request):
    
    if not request.user.is_staff:
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
            return render(request, './portafolios/create.html', {'form': form})
    return render(request, './portafolios/create.html', {'form': form})


@login_required
def add_comment_view(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()

    return redirect('portafolios:detail', id=project.id)


@login_required
def CreateEntryView(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Permisos
    if not request.user.is_staff or project.author != request.user:
        return messages.error("No tienes permiso para crear entradas.")

    if request.method == 'POST':
        form = CreateEntryForm(
            request.POST,
            request.FILES,
            project=project  # 👈 AQUÍ está la clave
        )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.project = project
            entry.save()
            messages.success(request, 'Entrada creada correctamente.')
            return redirect('portafolios:detail', project.id)
    else:
        form = CreateEntryForm(project=project)

    return render(request, 'portafolios/entry/create.html', {
        'form': form,
        'project': project
    })