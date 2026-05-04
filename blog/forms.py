from django import forms
from .models import BlogPost, Comment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["user", "text"]


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
