from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import fromstr
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.db.models import F

from .models import Post, Comment, Tag, IPAddress
from .forms import PostForm, CommentForm, ContactForm
from .utils import get_client_ip

from .helpers.sendgrid import send_mail



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# @cache_page(CACHE_TTL)
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

# @cache_page(CACHE_TTL)
def new_index(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	recent_posts = posts.order_by('-published_date')[:3]
	hot_posts = { hot_post:hot_post.approved_comments().count() for hot_post in posts if hot_post.approved_comments().count() > 0}
	sorted_hot_posts = dict(sorted(hot_posts.items(), key=lambda x: x[1], reverse=True))
	return render(request, 'blog/new_index.html', {'posts': posts, 'recent_posts': recent_posts, 'sorted_hot_posts': sorted_hot_posts})


def tag_posts(request, tag_slug):
	tag = Tag.objects.get(slug=tag_slug)
	posts = Post.objects.filter(tags=tag)
	return render(request, 'blog/tag_posts.html', {'posts':posts})

# @cache_page(CACHE_TTL)
def post_detail(request, pk):
	g = GeoIP2()
	post = get_object_or_404(Post, id=pk)
	ip_list = post.get_ip_list()
	user_ip = get_client_ip(request)
	location_info = g.city(str(user_ip))
	longitude, latitude, country = location_info['longitude'], location_info['latitude'], location_info['country_name']
	if not user_ip in ip_list:
		post.views = F('views') + 1
		ip_address, _ = IPAddress.objects.get_or_create(ip_address = user_ip, location = fromstr(f"POINT({longitude} {latitude})", srid=4326), country = country)
		post.ips.add(ip_address)
		post.save()
		post.refresh_from_db()
	return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form':form})


def drafts_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/drafts_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=post.pk)

@login_required
def post_delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')


def add_comment(request, pk):
	parent_post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = parent_post
			comment.save()
			return redirect('post_detail', pk=parent_post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment.html', {'form': form})

@login_required
def handle_comment(request, pk, action):
	comment = get_object_or_404(Comment, pk=pk)
	if action == "approve":
		comment.approve()
		return redirect('post_detail', pk=comment.post.pk)
	elif action == "delete":
		comment.delete()
		return redirect('post_detail', pk=comment.post.pk)


def contact_us(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		contact = form.save(commit=False)
		to = contact.email
		send_mail.delay(to=to)
		contact.save()
		return redirect('post_list')
	else:
		form = ContactForm()
	return render(request, 'blog/contact_us.html', {'form':form})
