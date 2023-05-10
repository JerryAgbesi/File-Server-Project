from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,HttpRequest
from .models import File
from .forms import SearchForm

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

def file_search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        files = File.objects.filter(title__icontains="" if query is None else query )
        return render(request,'fileapp/search.html',{'files':files})



