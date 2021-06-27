from django.db import models
from django.utils import timezone
from django.conf import settings


class Tag(models.Model):
	tag = models.CharField(max_length = 30)

	def __str__(self):
		return self.tag



class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	title = models.CharField(max_length = 100)
	text = models.TextField()
	created_date = models.DateTimeField(default = timezone.now)
	published_date = models.DateTimeField(blank = True, null = True)
	tags = models.ManyToManyField(Tag, related_name = 'tags', blank=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

	def approved_comments(self):
		return self.comments.filter(is_approved=True)


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.CharField(max_length = 100)
	text = models.TextField()
	created_date = models.DateTimeField(default = timezone.now)
	is_approved = models.BooleanField(default=False)

	def approve(self):
		self.is_approved = True
		self.save()

	def __str__(self):
		return self.text


class Contact(models.Model):
	name = models.CharField(max_length = 100)
	email = models.EmailField()
	subject = models.CharField(max_length = 100)
	message = models.TextField()

	def __str__(self):
		return self.name