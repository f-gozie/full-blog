from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
	post = get_object_or_404(Post, id=pk)
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