from django import forms
from .models import Project


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'git_url', 'tags']
        
        
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'image': 'Imagen',
            'git_url': 'URL del repositorio',
            'tags': 'Etiquetas',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'git_url': forms.URLInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }