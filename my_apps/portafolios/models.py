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
    
    
