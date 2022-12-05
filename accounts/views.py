
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from scheduling.models import Schedules, Scheduled
from django.contrib.auth import authenticate,login,logout
from .models import BasicAccount,IntervieweeAccount,InterviewerAccount
from .backend import EmailBackend
from mocx_2 import settings
from django.contrib.auth.decorators import login_required
import razorpay
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def home(request):
    context ={}
    schdeules = InterviewerAccount.objects.all
    check = Schedules.objects.all
    context['all']=schdeules
    context['dates']=check
    
     #Check The Interviewer filled all the deatils in InterviewerReg2
     #Better to Use boolean here!!!!!
    if IntervieweeAccount.Occupation is None:
        return redirect('IntervieweeReg')
    elif IntervieweeAccount.State is None:
        return redirect('IntervieweeReg')
    elif IntervieweeAccount.City is None:
        return redirect('IntervieweeReg')
    elif IntervieweeAccount.Residence is None:
        return redirect('IntervieweeReg')
    elif IntervieweeAccount.Res_city is None:
        return redirect('IntervieweeReg')
    else:
     return render(request,"accounts/index.html",context)  

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']
        #verfying user with backend DB
        user = EmailBackend.authenticate(email=email, password=pass1)
    
        if user is not None:
            login(request, user)
            schdeules = InterviewerAccount.objects.all
            check = Schedules.objects.all
            return render(request, "accounts/index.html",{'all':schdeules})
                
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
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST.get('Phone')
        
        if BasicAccount.objects.filter(email=email):
            messages.error(request, "email already exist! Please try some other email")
            return redirect('signup')
            
        if pass1 != pass2:
            messages.error(request,"Password does not match")
            return redirect('signup')

        #Creating User 
        if pass1==pass2:
            user = BasicAccount.objects.create_user(email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.phone=phone
            user.is_interviewer=False
            user.save()
            
            # Welcome Email to Registered User
            
            subject = "Welcome to MocX!"
            email_sub = "Account Activation for " + user.first_name
            message = "Hello" + ' ' + user.first_name + '!! \n' +'Welcome to MocX!! \n Hope you have some great things  done with our application to grow yourself!! \n\n Thanking You\n Team MocX' 
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True) #Send mail to the Registered Users!
            
            send_mail( # send one to ourselves as well when a new user registers
                         email_sub,
                         "has registered for an account, see subject",
                         'noreply@mocx.in',
                        ['mocx.mr@gmail.com'] 
                     )
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
        interviewee.City = City
        interviewee.State = State
        interviewee.Institute_name = Institute_name
        interviewee.Year_of_study = Year_of_study
        interviewee.Residence = Residence
        interviewee.Res_city = Res_city
        interviewee.save()
        return redirect("signin")
    return render(request,"accounts/IntervieweeReg.html", context = {"user":request.user.first_name} )

def InterviewerReg1(request):
    
    #Getting User info from Front-end
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST.get('Phone')
        
        if BasicAccount.objects.filter(email=email):
            messages.error(request, "email already exist! Please try some other email")
            return redirect('InterviewerReg1')
            
        if pass1 != pass2:
            messages.error(request,"Password does not match")
            return redirect('InterviewerReg1')

        #Creating User 
        if pass1==pass2:
            user = BasicAccount.objects.create_user(email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.phone=phone
            user.is_interviewer=True
            user.save()
            #Send Mail when interviewer creates an account!!
            subject = "Welcome to MocX!"
            email_sub = "Account Activation for " + user.first_name
            message = "Hello" + ' ' + user.first_name + '!! \n' +'Welcome to MocX!! \n Hope you have some great things  done with our application to grow yourself!! \n\n Thanking You\n Team MocX' 
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True) #Send mail to the Registered Users!
            
            send_mail( # send one to ourselves as well when a new user registers
                         email_sub,
                         "has registered for an account, see subject",
                         'noreply@mocx.in',
                        ['mocx.mr@gmail.com'] 
                     )
            login(request, user)
            return redirect('InterviewerReg2')
    return render(request,"accounts/InterviewerReg1.html")

def InterviewerReg2(request):
    
    interviewer = InterviewerAccount(uid = request.user)
    
    if request.method == "POST":
        age = request.POST['age']
        experience = request.POST['experience']
        price = request.POST['price']
        about_me = request.POST['about_me']
        linkedin = request.POST['linkedin']
        
        
        interviewer.Age = age
        interviewer.Experience = experience
        interviewer.Price = price
        interviewer.About_me = about_me
        interviewer.Linkedin = linkedin
        interviewer.save()
        return redirect('signin')
    return render(request,'accounts/InterviewerReg2.html')
    
   

def signout(request):
    logout(request)
    messages.success(request, "logged out!")
    return redirect("home")

@login_required
def view(request):
    #Create dictionary called context
    context={}
    
    #Get the requested interviewer Uid from the front-end
    id = request.GET['pid']
    
    #Get the Uid from Interviewer Table
    obj = Schedules.objects.filter(uid_id = id)
    bas = InterviewerAccount.objects.get(uid_id = id)
   
    #initilize context dictionary using "obj" and send it to the view.html.
    context["interviewer"]=obj
    context["basic"]=bas
    
    return render(request,"accounts/view.html",context)

@login_required
def confirm(request):
    if request.method == "POST":
        context = {}
        Student_uid = request.POST.get("ee_id")
        Interviewer_Slot = request.POST.get("slot_time")
        slot_id = request.POST.get("slot_id")
        ee_name = request.POST.get("ee_name")
        er_name = request.POST.get("er_name")
        price = request.POST.get('price')
        
        #Convert price from string to int 
        int_price = int(price)
        int_price=int_price*100
        
     
        #Razorpay stuff creating order and send it to server!!!!!
        client = razorpay.Client(auth =(settings.KEY , settings.SEC))
        payment = client.order.create({'amount':int_price , 'currency':'INR' , 'payment_capture': 1})
        client.set_app_details({"title" : "MocX", "version" : "1.3.8"})
        
        scheduled = Scheduled.objects.create(Student_uid_id=Student_uid, Interviewer_Slot_id=slot_id)
        scheduled.razor_pay_order_id = payment['id']
        scheduled.save()
        
        #test weather the created order_id is comming!!!!!
        print("**********")
        print(payment)
        print(int_price)
        print("**********")
        
        #Send it to the Confirmation page use Dictionary!!!
        context['item']=er_name
        context['slot']=Interviewer_Slot
        context['Student_uid']=Student_uid
        context['slot_id']=slot_id
        context['ee_name']=ee_name
        context['price']=price
        context['payment']=payment
        
    return render(request,"accounts/confirmation.html",context)

@login_required
def pay_success(request):
    if request.method == "GET":
     order_id = request.GET.get('order_id')
     scheduled = Scheduled.objects.get(razor_pay_order_id = order_id)
     #Check the detils of order_id and successful order_id was matching if same then payment is success!!!
     print(order_id)
     print(scheduled.razor_pay_order_id)
     
     #Change the payment status to Successful!!!
     scheduled.change_to_Successful()
     scheduled.save
     
     #Send email after Interviewee made payment successful!!
     subject = "Payment Successfull!"
     message = "Hello Team, \n\n\n" + 'Interviewee:  ' + scheduled.Student_uid.uid.first_name+'  ' + 'payment was successfull!! \n' +'with interviewer:  '+ scheduled.Interviewer_Slot.uid.uid.first_name +"\n"+"for the slot time and date:  "+str(scheduled.Interviewer_Slot.Slot_time)+'\n\n' +'Please Verify!!!'
     from_email = settings.EMAIL_HOST_USER
     to_list = ["rishikiranap@gmail.com"]
     send_mail(subject, message, from_email, to_list, fail_silently=True) #Send mail to the Registered Users!
     
     messages.success(request,"Payment Successful !!!")
     return render(request,"accounts/index.html")
     
    else:
        return HttpResponse('Payment Unsuccessful! Please try again')

def save_scheduled(request):
    pass
        
    return render(request,"accounts/confirmation.html")

    
@login_required
def delete(request, id): 
     #delete the slot added in the Scheduled Table if the user not willing to payment!!
     dele = Scheduled.objects.get(Interviewer_Slot_id=id)
     dele.delete()
     return redirect('home')
        
