from django.shortcuts import render,redirect
from newapp.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout

def index(request):
    return render(request,'index.html')

def register(request):
    registered=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            registered=True
        else:
            print(user_form)
    else:
        user_form=UserForm()
    return render(request,'registration.html',{'user_form':user_form,
                                                'registered':registered})


@login_required
def special(request):
    return HttpResponse("You are loged in")

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return HttpResponse("Account Not Active")
        else:
            print('some one tried to login and failed')
            print("username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details")
    else:
        return render(request,'login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

