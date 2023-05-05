from django.shortcuts import render
from django.views.generic import TemplateView
from .models import File

# Create your views here.

class HomeView(TemplateView):
    template_name = "fileapp/home.html"
