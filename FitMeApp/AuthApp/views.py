from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


def Home(request):
    return render(request,"home.html")

def Workout(request):
    return render(request,"new.html")

def signup(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
   
        if pass1!=pass2: 
            messages.info(request,"Password is not Matching")
            return redirect('/signup')
        
        try:     
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username is taken")
                return redirect('/signup')
        except Exception as identifier:
            pass
        try: 
            if User.objects.get(email=email):
                messages.warning(request,"Email is Taken")
                return redirect('/signup')
        except Exception as identifier:
            pass
            
        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,"User is Created Please Login")
        return redirect('/login')
    
    return render(request,"signup.html")

def handlelogin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        pass1=request.POST.get('pass1')
        myuser=authenticate(username=username,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Successful")
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/login")

    return render(request,"handlelogin.html")


def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/login')


