from  django import forms
from .models import Post, Comment
from django.forms.widgets import ClearableFileInput

class PostCreateForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ('title', 'category', 'bill', 'event', 'excerpt', 'body')
        # fields  = ('title', 'category', 'tag', 'bill', 'event', 'excerpt', 'body', 'image')
        widgets = {
            'title':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter title of new post'}),
            # 'author':   forms.Select(    attrs={'class': 'form-control', 'type':'hidden'}),
            'category': forms.Select(   attrs={'class': 'form-control'}),
            # 'tag':      forms.Select(    attrs={'class': 'form-control'}),
            'bill':     forms.Select(   attrs={'class': 'form-control'}),
            'event':    forms.Select(   attrs={'class': 'form-control'}),
            'excerpt':  forms.TextInput(attrs={'class': 'form-control'}),
            'body':     forms.Textarea( attrs={'class': 'form-control'}),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ('title', 'category', 'bill', 'event', 'excerpt', 'body')
        # fields = ('title', 'category', 'tag', 'excerpt', 'body', 'image')
    
        widgets = {
            'title':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter title of new post'}),
            'category': forms.Select(   attrs={'class': 'form-control'}),
            # 'tag':      forms.Select(   attrs={'class': 'form-control'}),
            'bill':     forms.Select(   attrs={'class': 'form-control'}),
            'event':    forms.Select(   attrs={'class': 'form-control'}),
            'excerpt':  forms.TextInput(attrs={'class': 'form-control'}),
            'body':     forms.Textarea( attrs={'class': 'form-control'}),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model   = Comment
        fields  = ('body',)
        widgets = {
            'body':  forms.Textarea( attrs={'class': 'form-control'}),
        }

