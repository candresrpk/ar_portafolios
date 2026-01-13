from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        
    def __str__(self):
        return f'{self.name}'


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='portafolio/images/')
    git_url = models.URLField(blank=True)
    top = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        
    
    def __str__(self):
        return f'{self.title}'
    
    
    @property
    def total_likes(self):
        return Like.objects.filter(project=self).count()
    
    @property
    def total_comments(self):
        return Comment.objects.filter(project=self).count()
    
    @property
    def total_views(self):
        return View.objects.filter(project=self).count()
    
    @property
    def is_top(self):
        return self.top
    
    
    
class Like(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['project', 'user']
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        
    def __str__(self):
        return f'{self.project} - {self.user}'
    
    
class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        
    def __str__(self):
        return f'{self.user} - {self.project} - {self.content}'
    
    

class View(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name = 'Vista'
        verbose_name_plural = 'Vistas'
        
    def __str__(self):
        return f'{self.project} - {self.user}'
    

    
    
### crear modelo para mostrar contenido readme dentro del proyecto
### es decir, se va a mostrar instrucciones de manejar el proyecto
### con imagenes
### codigo
### texto explicativo del proyecto
### link al git del proyecto



class Entry(models.Model):

    class ContentTypes(models.TextChoices):
        TEXT = 'text'
        IMAGE = 'image'
        CODE = 'code'
        LINK = 'link'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="entries"
    )
    order = models.PositiveIntegerField()
    content_type = models.CharField(
        max_length=10,
        choices=ContentTypes.choices,
        default=ContentTypes.TEXT
    )
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='portafolio/content/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'order'],
                name='unique_entry_order_per_project'
            )
        ]

    def __str__(self):
        return f'{self.project} | Entrada #{self.order}'
