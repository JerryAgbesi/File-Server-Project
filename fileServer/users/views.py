from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from users.forms import EmailAuthenticationForm
from django.contrib.auth.views import LoginView
from .forms import UserSignUpForm


 
def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # username = form.cleaned_data.get('username')
            new_user = authenticate(email=form.cleaned_data.get('email'),password=form.cleaned_data.get('password2'))
            login(request,new_user)
            return redirect('home')
            
            
    else:
        form = UserSignUpForm( )
    return render(request,"users/signup.html",{'form':form})
    
class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
  
