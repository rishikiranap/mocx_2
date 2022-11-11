
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import BasicAccount,IntervieweeAccount
from .backend import EmailBackend
# Create your views here.

def home(request):
    #Check if user has filled is details else redirect to intervieweereg or interviewerreg 
    return render(request,"accounts/index.html")

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']
        #verfying user with backend DB
        user = EmailBackend.authenticate(email=email, password=pass1)
    
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
        phone = request.POST.get('Phone')

        #Creating User 
        if pass1==pass2:
            user = BasicAccount.objects.create_user(email, username, pass1)
            user.first_name = fname
            user.last_name = lname
            user.phone=phone
            user.save()
            login(request, user)
            return redirect('IntervieweeReg')
    return render(request,"accounts/signup.html")

#Show these details if interviewee is logged in
#use @login_required decorated to check if user is logged in
def IntervieweeReg(request):
    
    interviewee = IntervieweeAccount(uid = request.user)
    
    if request.method == "POST":
        Occupation = request.POST['Occupation']
        Company = request.POST['Company']
        Institute_name = request.POST['Institute_name']
        Year_of_study = request.POST.get('Year_of_study')
        State = request.POST['State']
        City = request.POST['City']
        Residence = request.POST['Residence']
        Res_city = request.POST['Res_city']
        
         
        #Pushing Into intervieweeAccount Table
         
        interviewee.Occupation = Occupation
        interviewee.Company = Company
        interviewee.City=City
        interviewee.State=State
        interviewee.Institute_name = Institute_name
        interviewee.Year_of_study = Year_of_study
        interviewee.Residence = Residence
        interviewee.Res_city = Res_city
        interviewee.save()
        return redirect("signin")
    return render(request,"accounts/IntervieweeReg.html", context = {"user":request.user.first_name} )

        

def signout(request):
    logout(request)
    messages.success(request, "logged out!")
    return redirect("home")