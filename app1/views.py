from django.shortcuts import render
from app1.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

from django.contrib.auth.decorators import  login_required


# Create your views here.
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        
        return render(request,'home.html',d)
    return render(request,'home.html')

def register(request):
    UF=UserForm()
    PF=ProfileForm()
    d={'uf':UF,'pf':PF}

    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)

        if UFD.is_valid() and PFD.is_valid():
            UFO=UFD.save(commit=False)
            password=UFD.cleaned_data['password']
            UFO.set_password(password)
            UFO.save()

            PFO=PFD.save(commit=False)
            PFO.profile_user=UFO
            PFO.save()

            
            send_mail('register',
            'Thanks for registration.',
            'sivabokam7482@gmail.com',
            [UFO.email],fail_silently=False
            )

            return HttpResponse('Registration Successfully')

    return render(request,'Registration.html',d)



def userlogin(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)
        
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('Home'))
        else:
            return HttpResponse('you are not an authenticated user')

    return render(request,'user_login.html')

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))

@login_required
def profiledisplay(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(profile_user=UO)
    d={'uo':UO,'po':PO}
    return render(request,'profile_display.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['password']

        un=request.session.get('username')
        UO=User.objects.get(username=un)

        UO.set_password(pw)
        UO.save()
        return HttpResponse('password is changed successfully')

    return render(request,'changepassword.html')

def reset_password(request):
   
   if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)

        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password reset is Done')
        else:
            return HttpResponse('user is not present in my DataBase')
        

     
        
   return render(request,'resetpassword.html')