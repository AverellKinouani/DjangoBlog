from django.contrib import admin
from .models import Category, Comment, Post, Profile, Images


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Images)
admin.site.register(Profile)
