from django import forms
from .models import Post, Comment, Contact
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(forms.ModelForm):
	text = forms.CharField(widget=CKEditorUploadingWidget(extra_plugins=['youtube', 'html5video']))
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