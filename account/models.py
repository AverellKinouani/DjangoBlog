from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = RichTextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True)
    phone_number = PhoneNumberField(blank=True)


    def __str__(self):
        return 'Profile of user {}'.format(str(self.user.username))


    def save(self, *args, **kwargs):
    	super().save(*args, **kwargs)

    	img = Image.open(self.image.path)
    	if img.height > 300 or img.width > 300:
    		output_size = (300, 300)
    		img.thumbnail(output_size)
    		img.save(self.image.path)

