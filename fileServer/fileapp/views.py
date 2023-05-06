from django.shortcuts import render
from django.views.generic import TemplateView
from .models import File

files = [
    {
        'title': "Wedding invite",
        'description': 'wedding invite for Eric and Vera',
        'date_uploaded': 'May 7, 2022',
        'number_of_emails': '0',
        'number_of_downloads': '0'

    },
    {
        'title': "Funeral Brochure",
        'description': 'Funeral brochure of ..',
        'date_uploaded': 'May 19, 2022',
        'number_of_emails': '0',
        'number_of_downloads': '0'
 
    }
]

class HomeView(TemplateView):
    template_name = "fileapp/home.html"
    extra_context = {"files":files}
