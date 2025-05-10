from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg', 'placeholder': 'Enter your blog title'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-lg', 'rows': 10, 'placeholder': 'Write your blog content here'}),
        }