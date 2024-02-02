from django.contrib import admin

from .models import Video, Category, Comment

# Register your models here.
admin.site.register([Video,Category, Comment])