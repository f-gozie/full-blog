from django.urls import path
from . import views


urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/edit/<int:pk>', views.post_edit, name='post_edit'),
	path('drafts/', views.drafts_list, name='drafts_list'),
	path('post/<int:pk>/publish', views.post_publish, name='post_publish'),
	path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
	path('post/<int:pk>/comment/add', views.add_comment, name='add_comment'),
	path('post/<int:pk>/comment/<str:action>', views.handle_comment, name='handle_comment'),
	path('contact_us/', views.contact_us, name='contact_us'),
	path('tag/<str:tag_slug>/posts', views.tag_posts, name='tag_posts'),
	path('new_index/', views.new_index, name='index')
]