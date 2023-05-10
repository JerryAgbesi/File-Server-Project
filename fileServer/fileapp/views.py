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
  
    # form = SearchForm(request.GET)
    # results = []

    # if form.is_valid():
    #     query = form.cleaned_data['query']
    #     results = File.objects.filter(name__icontains=query) | File.objects.filter(description__icontains=query)

    # context = {
    #     'form': form,
    #     'files': results,
    # }

    # return render(request, 'fileapp/search.html')

    if request.method == 'GET':
        query = request.GET.get('search')
        print(query)
        files = File.objects.filter(title__icontains="" if query is None else query )
        return render(request,'fileapp/search.html',{'files':files})

    # if request.GET.get('search'):
    #     file_title = request.GET.get('search')
    #     try:
    #         status = File.objects.filter(title_icontains=file_title)
    #         print(f'1:{status}')
    #         return render(request,'search.html',{'files':status})
    #     except:
    #         print(f'2:{status}')
    #         return render(request,'search.html',{'files':status})
    # else:
    #     print(f'3:{status}')
    #     return render(request,'search.html',{'files':status})    


