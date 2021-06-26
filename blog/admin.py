from django.contrib import admin
from .models import Post, Comment, Contact


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'
	list_display = ['id', 'author', 'title', 'text', 'created_date', 'published_date']
	fieldsets = (
		(None, {
			'fields': ('author', 'title', 'text'),
		}),
		('Advanced Options', {
			'classes': ('collapse',),
			'fields': ('created_date', 'published_date'),
		}),
	)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	pass

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'subject']
	readonly_fields = ('name', 'email', 'subject', 'message')