
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def home(request):
    return render(request,"accounts/index.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        #verfying user with backend DB
        user = authenticate(username=username, password=pass1)
    
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "accounts/index.html", {"fname": fname})
        
        else:
            messages.error(request, "Invalid User")
            return redirect('home')
    return render(request,"accounts/signin.html")

def signup(request):
    #if user aldready logged in then

    if request.user.is_authenticated:
        return redirect(f'/{request.user.username}')

    #Getting User info from Front-end
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        Phone = request.POST.get('Phone')

        #Creating User 
        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.save()
        messages.success(request, "Account Created")
        return redirect('signin')
    return render(request,"accounts/signup.html")

def signout(request):
    logout(request)
    messages.success(request, "logged out!")
    return redirect("home")