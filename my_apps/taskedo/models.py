from django.db import models
from django.core.exceptions import ValidationError
from my_apps.usuarios.models import Organization, Profile
# Create your models here.


class Project(models.Model):
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        
        
    def __str__(self):
        return f'{self.title} by {self.author}'
    
    
class Task(models.Model):
    
    class PriorityChoices(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        
    class StatusChoices(models.IntegerChoices):
        TODO = 1, 'To Do'
        IN_PROGRESS = 2, 'In Progress'
        DONE = 3, 'Done'
    
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tasks')
    
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    priority = models.IntegerField(choices=PriorityChoices.choices, default=PriorityChoices.LOW)
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
        indexes = [
            models.Index(fields=['priority', 'status']),
        ]
        
        
    def __str__(self):
        return f'{self.title} assigned to {self.owner}'
    
    def clean(self):
        if not self.project.organization.members.filter(id=self.owner.id).exists():
            raise ValidationError("El usuario no pertenece a la organización del proyecto")

        if self.parent == self:
            raise ValidationError("Una tarea no puede ser padre de sí misma")
        
        if self.parent and self.parent.project != self.project:
            raise ValidationError("La tarea padre debe pertenecer al mismo proyecto")
        
        if self.parent and self.parent.status == Task.StatusChoices.DONE:
            raise ValidationError("No se puede crear una tarea hija de una tarea finalizada")
        
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)