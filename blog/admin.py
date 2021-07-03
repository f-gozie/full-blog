from django.contrib import admin
from .models import Post, Comment, Contact, Tag, Category, IPAddress
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
	list_display = ['title','author', 'views', 'category', 'created_date', 'published_date', 'get_tags', 'display_img']
	list_display_links = ['title']
	fieldsets = (
		(None, {
			'fields': ('author', 'title', 'category', 'text', 'tags', 'display_img'),
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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
# 	Column Methods
	def get_posts(self, obj):
		return len([post for post in obj.posts.all()])

	get_posts.short_description = "No of Posts"
	list_display = ['category', 'get_posts']


@admin.register(IPAddress)
class IPAddressClass(admin.ModelAdmin):
	list_display = ['ip_address']