from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from my_apps.blog.models import Post, Tag, PostContent
from my_apps.blog.forms import CreatePostForm, ContentForm
from django.contrib import messages

def PostListView(request):
    
    tag_slug = request.GET.get('tag')

    posts = (
        Post.objects
        .select_related('author')
        .prefetch_related('tags')
        .order_by('-created_at')
    )

    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    # PAGINACIÓN
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'tags': Tag.objects.all(),
        'active_tag': active_tag,
    }
    
    return render(request, './blog.html', context)


@login_required
def createPostView(request):

    
    if not request.user.is_staff:
        messages.error(
            request,
            '❌ No tienes permisos para crear posts.'
        )
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)  # 🔥 AQUÍ
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            messages.success(request, '✅ Post creado correctamente.')
            return redirect('blog:post_list')
        else:
            messages.error(request, '❌ Hay errores en el formulario.')
    else:
        form = CreatePostForm()
    return render(request, 'posts/create.html', {
        'form': form
    })
    
    
def postDetailView(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('tags'),
        slug=slug
    )

    contents = (
        PostContent.objects
        .filter(post=post)
        .order_by('order')
    )

    context = {
        'post': post,
        'contents': contents,
    }
    return render(request, 'posts/detail.html', context)



def createEntryView(request, id):
    
    post = get_object_or_404(Post, id=id)
    
    if request.user != post.author:
        messages.error(request, 'No tienes permisos para agregar entradas.')
        return redirect(post.get_absolute_url())
    
    context = {
        'post': post
    }
    if request.method == 'POST':
        form = ContentForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            content = form.save(commit=False)
            content.post = post
            content.save()
            messages.success(request, 'Entrada creada correctamente.')
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, '❌ Hay errores en el formulario.')
            context['form'] = form
            return render(request, 'posts/entry/create.html', context)
    else:
        form = ContentForm()
        context['form'] = form
    return render(request, 'posts/entry/create.html', context)