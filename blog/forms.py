from django import forms
from .models import Post, Comment, Contact


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'text',)


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('author', 'text')


class ContactForm(forms.ModelForm):

	class Meta:
		model = Contact
		fields = '__all__'