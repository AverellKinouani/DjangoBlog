from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.db.models.signals import post_save
from django.dispatch import receiver


STATUS = (('draft', 'Draft'),
          ('published', 'Published'))


class Author(models.Model):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    slug = models.SlugField(max_length=100, unique=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=200)
    picture = models.ImageField(default='default.jpg', upload_to='posts_pics')
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    publish_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True)
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish_at',)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog-post-detail',
                       args=[self.publish_at.year,
                             self.publish_at.month,
                             self.publish_at.day,
                             self.slug])

class Images(models.Model):
    picture = models.ImageField(default='default.jpg', upload_to='posts_pics')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Images'

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    content = models.TextField(
        max_length=200, blank=False, null=False, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True)
    email = models.EmailField()

    def __str__(self):
        return 'Profile of user {}'.format(str(self.user.username))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)