from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='projects')
    
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        
        
    def __str__(self):
        return f'{self.title} by {self.author}'
    
    
class Task(models.Model):
    
    class ProrityChoices(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        
    class StatusChoices(models.IntegerChoices):
        TODO = 1, 'To Do'
        IN_PROGRESS = 2, 'In Progress'
        DONE = 3, 'Done'
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False, related_name='project_tasks')
    
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    priority = models.IntegerField(choices=ProrityChoices.choices, default=ProrityChoices.LOW)
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.TODO)
    
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority','created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        
    def __str__(self):
        return f'{self.title} assigned to {self.owner}'