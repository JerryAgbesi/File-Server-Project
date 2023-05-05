from django.contrib import admin
from .models import File

# Register File model to show files on the admin page
admin.site.register(File)