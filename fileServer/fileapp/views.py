from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import File

#Ensure users are authenticated before accessing pages.
#This explains the reason for the mixin 
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "fileapp/home.html"
    extra_context = {"files":File.objects.all()}
    

def file_download(request,file_id):
    file = get_object_or_404(File,pk=file_id)
    file.number_of_downloads += 1
    file.save()
    response = HttpResponse(file.file,content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    
    return response

#function to increase number of downloads 
# def increment_downloads(request,file_id):
#     file = get_object_or_404(File,pk=file_id)
#     file.number_of_downloads += 1
