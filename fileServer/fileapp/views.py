from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,HttpRequest
from django.conf import settings
import requests
from .models import File
from .forms import EmailForm
import boto3
from botocore.exceptions import ClientError
import magic


#Ensure users are authenticated before accessing pages.
#This explains the reason for the mixin 
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "fileapp/home.html"
    extra_context = {"files":File.objects.all()}
    

def generate_presigned_url(bucket_name,object_name,expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket':bucket_name,"Key":object_name},ExpiresIn=expiration
        )
    except ClientError as e:
        return None

    return response    

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

class EmailForm(TemplateView):
    template_name = "fileapp/send_mail.html"
    extra_context = {"form":EmailForm}   

def email_form(request,file_id):
    form = EmailForm
    file = get_object_or_404(File,pk=file_id)
    return render(request,"fileapp/send_mail.html",{'form':form,"file":file})    

def preview_file(request,file_id):
    file_obj = File.objects.get(id=file_id)
  


    file_url = file_obj.file.url

    #Get the content of the file
    response = requests.get(file_url)

    content_type = response.headers['Content-Type']
    response_headers = {
        'Content-Disposition':'inline',
    }

    return HttpResponse(response.content, content_type=content_type, headers=response_headers)


def send_mail(request,file_id):
    file = get_object_or_404(File,pk=file_id)
    if request.method == "POST":
        form = EmailForm(request.POST,request.FILES)
        print(form.cleaned_data['subject'])

        if form.is_valid:
            email = EmailMessage(
                form.cleaned_data['subject'],
                form.cleaned_data['body'],
                settings.EMAIL_HOST_USER,
                form.cleaned_data['to'])
        # print(form.cleaned_data['subject'])
            # email.attach(
            #     file.title,
            #     file.read(),
            #     file.content_type)
            # email.send()


            

