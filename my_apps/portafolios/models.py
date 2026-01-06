from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='portafolio/images/')
    git_url = models.URLField(blank=True)
    top = models.BooleanField(default=False)

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
        return f'{self.user} - {self.project}'
    
    

class View(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['project', 'user']
        verbose_name = 'Vista'
        verbose_name_plural = 'Vistas'
        
    def __str__(self):
        return f'{self.project} - {self.user}'
    
    
    