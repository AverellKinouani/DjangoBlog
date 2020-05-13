from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts_list, name='blog-home'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', views.post_detail, name='post_detail'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
    path('categorie/<slug:slug>', views.category_posts, name='category'),
    path('search/', views.search, name='search'),
    path('tag/<str:tag>', views.tag, name='tag'),
    path('creer-un-article', views.create_post, name='create_post'),
    path('modifier-un-article/<int:year>/<int:month>/<int:day>/<slug:slug>', views.update_post, name='update_post'),
]
