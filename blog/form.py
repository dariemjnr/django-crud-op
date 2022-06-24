from dataclasses import fields
from turtle import title
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'body',
            'status',

        ]
    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if title.endswith('edu'):
    #         raise forms.ValidationError('This title already exist!! kindly rename your title')
