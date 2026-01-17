from django import forms
from my_apps.blog.models import Post, PostContent, Tag


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'tags']
        labels = {
            'title': 'Título',
            'body': 'Contenido',
            'image': 'Imagen',
            'tags': 'Etiquetas',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
    
    
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Nombre',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    
    def validate_tag(self):
        tag_name = self.cleaned_data['name']
        existing_tag = Tag.objects.filter(name=tag_name).first()
        if existing_tag:
            raise forms.ValidationError("Ya existe una etiqueta con el mismo nombre.")
        return tag_name
    
    
    
    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(' ', '-')
        super(Tag, self).save(*args, **kwargs)
        
        

class ContentForm(forms.ModelForm):
    class Meta:
        model = PostContent
        fields = ['title','content_type', 'content', 'image']
        
        labels = {
            'title': 'Título',
            'content_type': 'Tipo de contenido',
            'content': 'Contenido',
            'image': 'Imagen',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
