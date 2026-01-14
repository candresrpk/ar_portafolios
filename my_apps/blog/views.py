from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from my_apps.blog.models import Post, Tag


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