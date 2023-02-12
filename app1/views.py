from django.shortcuts import render
from app1.forms import *
from django.http import HttpResponse
# Create your views here.
def home(request):
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
            return HttpResponse('Registration Successfully')

    return render(request,'Registration.html',d)