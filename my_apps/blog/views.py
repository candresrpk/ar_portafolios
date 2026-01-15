from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from my_apps.blog.models import Post, Tag
from my_apps.blog.forms import CreatePostForm
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
    
    return render(request, './blog/posts.html', context)


@login_required
def create_post_view(request):

    
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
    return render(request, 'blog/create.html', {
        'form': form
    })