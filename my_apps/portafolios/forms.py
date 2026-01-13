from django import forms
from .models import Project, Entry, Comment


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
        
        

class CreateEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Entry
        fields = ['order', 'content_type', 'content', 'image']

        labels = {
            'order': 'Orden',
            'content_type': 'Tipo de contenido',
            'content': 'Contenido',
            'image': 'Imagen',
        }

        widgets = {
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_order(self):
        order = self.cleaned_data.get('order')

        if self.project and Entry.objects.filter(
            project=self.project,
            order=order
        ).exists():
            raise forms.ValidationError(
                f'Ya existe una entrada con el orden {order} para este proyecto.'
            )

        return order

    def clean(self):
        cleaned_data = super().clean()

        content_type = cleaned_data.get('content_type')
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')

        if content_type == Entry.ContentTypes.IMAGE and not image:
            raise forms.ValidationError(
                'Debes subir una imagen para este tipo de contenido.'
            )

        if content_type in [
            Entry.ContentTypes.TEXT,
            Entry.ContentTypes.CODE,
            Entry.ContentTypes.LINK
        ] and not content:
            raise forms.ValidationError(
                'Este tipo de contenido requiere texto.'
            )

        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario...'
            }),
        }