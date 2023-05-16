from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from users.forms import EmailAuthenticationForm
from django.contrib.auth.views import LoginView
from .forms import UserSignUpForm


 
def signup(request):
    

    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
            
    else:
        form = UserSignUpForm( )
    return render(request,"users/signup.html",{'form':form})
    
class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
  
