from django.contrib import admin
from .models import Post, Comment, Contact, Tag
from .forms import PostForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

	# Column Methods
	def get_tags(self, obj):
		return [tag for tag in obj.tags.all()]

	# Admin Config
	form = PostForm
	filter_horizontal = ['tags']
	empty_value_display = '-empty-'
	get_tags.short_description = 'Tags'
	list_display = ['id', 'author', 'title', 'created_date', 'published_date', 'get_tags']
	fieldsets = (
		(None, {
			'fields': ('author', 'title', 'text', 'tags'),
		}),
		('Advanced Options', {
			'classes': ('collapse',),
			'fields': ('created_date', 'published_date'),
		}),
	)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	pass


@admin.register(Tag)
class CommentAdmin(admin.ModelAdmin):
	pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'subject']
	readonly_fields = ('name', 'email', 'subject', 'message')