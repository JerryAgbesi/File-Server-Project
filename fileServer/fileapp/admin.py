from django.contrib import admin
from .models import File
from django.contrib.auth.models import User

# Register File model to show files on the admin page
admin.site.register(File)
admin.site.register(User)