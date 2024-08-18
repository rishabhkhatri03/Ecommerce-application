from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.views import View
from .utils import generate_token
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        
        # Check if passwords match
        if password != confirm_password:
            messages.warning(request, "Passwords do not match.")
            return render(request, 'authentication/signup.html', {'email': email})

        try:
            if User.objects.get(username=email):
                messages.info(request,"Email is taken")
                return render(request, 'authentication/signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        email_subject = "Activate your Account"
        message = render_to_string('authentication/activation_email.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })
        
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        email_message.send()
        messages.success(request,"Activate your account by clicking the link in your mail.")
        return redirect('/auth/signup/')
    return render(request, 'authentication/signup.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request,"Account activated successfully.")
            return redirect('/auth/login/')
        return redirect('/auth/signup/')

def handlelogin(request):
    if request.method=="POST":
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username, password=userpassword)
        
        if myuser is not None:
            login(request,myuser)
            messages.success(request, "Login Successfully")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('/auth/login/')
    return render(request, 'authentication/login.html')


def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Success")
    return redirect('/auth/login')