from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from users.forms import EmailAuthenticationForm
from django.contrib.auth.views import LoginView
from .forms import UserSignUpForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .tokens import account_activation_token
from django.contrib.auth import get_user_model


def activate(request,uidb64,token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user =None    
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()

        messages.success(request,"Thank you for confirming your email, You may now go ahead and log in.")
        return redirect('login')
    else:
        messages.error(request,"Activation link is invalid")

    return redirect('home')



def activateEmail(request,user,to_email):
    mail_subject = "activate your account"
    message = render_to_string('users/activate_account.html',{
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    
    email = EmailMessage(mail_subject,message,to=[to_email])

    if email.send():
        messages.success(request,f'Kindly check your inbox at {to_email} to activate your account')
    else:
        messages.error(request, f'Problem sending email to {to_email}, please check on the email and try again')    
 
def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit = False)
            new_user.is_active= False
            new_user.save()
            # username = form.cleaned_data.get('username')
            # new_user = authenticate(email=form.cleaned_data.get('email'),password=form.cleaned_data.get('password2'))
            # login(request,new_user)
            activateEmail(request,new_user,form.cleaned_data.get('email'))
            return redirect('home')
            
            
    else:
        form = UserSignUpForm( )
    return render(request,"users/signup.html",{'form':form})
    
class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
  
