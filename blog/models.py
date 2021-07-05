# from django.db import models
from django.contrib.gis.db import models
from django.utils import timezone
from django.conf import settings

from autoslug import AutoSlugField


class Tag(models.Model):
	tag = models.CharField(max_length = 50)
	slug = AutoSlugField(null = True, default = None, unique = True, populate_from='tag')

	def __str__(self):
		return self.tag

class Category(models.Model):
	category = models.CharField(max_length = 50)

	class Meta:
		verbose_name_plural = "Categories"


	def __str__(self):
		return self.category


class IPAddress(models.Model):
	ip_address = models.GenericIPAddressField()
	location = models.PointField(null=True)
	country = models.CharField(max_length = 50, null = True)

	class Meta:
		verbose_name_plural = "IP Addresses"

	def __str__(self):
		return self.ip_address

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	title = models.CharField(max_length = 100)
	text = models.TextField()
	created_date = models.DateTimeField(default = timezone.now)
	published_date = models.DateTimeField(blank = True, null = True)
	tags = models.ManyToManyField(Tag, related_name = 'posts', blank=True)
	display_img = models.ImageField(upload_to = 'displays')
	category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name='posts')
	views = models.PositiveIntegerField(default=0)
	ips = models.ManyToManyField(IPAddress, related_name = 'posts', blank = True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

	def approved_comments(self):
		return self.comments.filter(is_approved=True)

	def get_ip_list(self):
		return [ip.ip_address for ip in self.ips.all() ]

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