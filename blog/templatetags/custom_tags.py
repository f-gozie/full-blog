from django import template
from blog.models import Tag
from django.template.defaulttags import register

register = template.Library()

@register.filter
def get_value(dictionary, key):
	return dictionary.get(key)

@register.simple_tag
def get_tags():
	return Tag.objects.all()