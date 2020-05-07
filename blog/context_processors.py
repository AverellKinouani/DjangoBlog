from django.conf import settings
from .models import Category, Post
from taggit.models import Tag


def categories(request):
	categories = Category.published.all()
	return {'categories': categories}


def tags(request):
	tags = Tag.objects.all()
	return {'tags': tags}


def last_posts(request):
	last_posts = Post.published.all()[:3]
	return {'last_posts': last_posts}