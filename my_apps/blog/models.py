from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['created_at']
        
    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(' ', '-')
        super(Tag, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name
    
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    image = models.ImageField(
        upload_to='blog/posts/',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    tags = models.ManyToManyField(Tag, blank=True)
    
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['created_at']
        
    
    
    def save(self, *args, **kwargs):
        self.slug = self.title.lower().replace(' ', '-')
        super(Post, self).save(*args, **kwargs)
    
    
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail', args=[self.slug])   
    
    
    def __str__(self):
        return self.title
    
    
    
class PostContent(models.Model):
    
    class ContentTypes(models.TextChoices):
        TEXT = 'text'
        IMAGE = 'image'
        CODE = 'code'
        LINK = 'link'
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField()
    content_type = models.CharField(
        max_length=10,
        choices=ContentTypes.choices,
        default=ContentTypes.TEXT
    )
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='blog/content/',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['order']
        
        
    def __str__(self):
        return f'{self.post} | Entrada #{self.order}'
    