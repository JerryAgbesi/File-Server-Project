from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db import close_old_connections
import requests
from .models import File
from .forms import EmailForm
import boto3


#Ensure users are authenticated before accessing pages.
#This explains the reason for the mixin 
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "fileapp/home.html"
    close_old_connections()
    extra_context = {"files":File.objects.all().order_by('date_uploaded')}

def file_download(request,file_id):
    file = get_object_or_404(File,pk=file_id)
    file_url = file.file.url

    #increment the number of downloads 
    file.number_of_downloads += 1
    file.save()

    #Get the content and content type of the file
    response = requests.get(file_url)

    content_type = response.headers['Content-Type']
    response = HttpResponse(file.file,content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    
    return response

def file_search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        files = File.objects.filter(title__icontains= ""  if query is None else query) | File.objects.filter(description__icontains= ""  if query is None else query)
        return render(request,'fileapp/search.html',{'files':files})

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
        if request.method == 'POST':
            form = EmailForm(request.POST)
            file_obj = File.objects.get(id=file_id)
            file_url = file_obj.file.url


            if form.is_valid():
                # mail = form.save(commit=False)
                

                #Retrieve the file from the S3 bucket
                s3 = boto3.resource('s3')
                bucket_name = 'django-file-server'

                bucket_url = f'https://{bucket_name}.s3.amazonaws.com/'
                file_path = file_url.replace(bucket_url, '')

                # Remove query parameters if present
                file_path = file_path.split('?')[0]

                file_key = file_path
                file_object = s3.Object(bucket_name,file_key)
                file_content = file_object.get()['Body'].read()

                email = EmailMessage(
                    subject = form.cleaned_data['subject'],
                    body = form.cleaned_data['body'],
                    from_email= 'noreply@fileserver.com',
                    to = [form.cleaned_data['to']],headers={'From': 'File Server <noreply@fileserver.com>'})
                
                response = requests.get(file_url)


                #Determine the content type of the file being attached
                content_type = response.headers['Content-Type']
                
                #attach file content to email being sent
                email.attach(file_obj.title,file_content,content_type)

                
                email.send()

                #Increase the count emails sent for the file
                file_obj.number_of_emails += 1
                file_obj.save()

                messages.success(request,'File has been sent succesfully')
                
                return redirect('home')
                
        else:
            form = EmailForm()
            

        return render(request,'send_mail.html',{'form':form})    

            

