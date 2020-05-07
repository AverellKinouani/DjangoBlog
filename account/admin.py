from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'image', 'bio', 'location', 'phone_number')

admin.site.register(Profile, ProfileAdmin)
