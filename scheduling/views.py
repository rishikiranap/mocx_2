from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.models import InterviewerAccount,BasicAccount
from .models import Schedules
from accounts.backend import EmailBackend
from mocx_2 import settings
from django.core.mail import send_mail
from datetime import datetime,timezone
import datetime
from pytz import timezone


# Create your views here.
#adding mock interview's time slots by the interviewer
@login_required
def add_slot(request):
    if request.method == 'POST':
       # TODO:Need to covert into IST from UTC !!!!!
        Slot = request.POST['Slot_TimeDate']
    
    
        #Getting Uid from InterviewerAccount linked with BasicAccount
        interviewer = InterviewerAccount.objects.get(uid = request.user)
        add_slot = Schedules(uid = interviewer)
        add_slot.Slot_time = Slot
        
        
        #Gettimg the local time 
        current_time = datetime.datetime.now()
        
        #Formating the local time as per input slot time and date formate
        time_now = current_time.strftime("%Y-%m-%dT%H:%M")
     
        #Interviewer cannot Select a Slot which is outdated
        if Slot < time_now:
            print("error")
            messages.error(request,"error::Selected time and date is Past!!!")
            return redirect('add_slot')
        elif Slot == time_now:
            messages.error(request,"error::Action cannot be performed!!")
            return redirect('add_slot')
        
        add_slot.change_to_added()
        add_slot.save()
        
        #Send email when new time slot is added by the Interviewer
        
       # subject = "Timeslot added succesfully!"
        #email_sub = "Added new time-slot " + user.first_name
        #message = "Hello" + ' ' + user.first_name + '!! \n' +'Time-slot' + Schedules.Slot_time + 'added succesfully!' '\n if not you contact team MocX\n\n Thanking You\n Team MocX' 
        #from_email = settings.EMAIL_HOST_USER
        #to_list = [user.email]
        #send_mail(subject, message, from_email, to_list, fail_silently=True) #Send mail to the Interviewer!
            
        #send_mail( # send one to ourselves when a new time slot is added by the interviewer!!
                      #   email_sub,
                       #  "has added a new time-slot, see subject",
                        # 'noreply@mocx.in',
                        #['mocx.mr@gmail.com'] 
                     #)
            
        #return redirect("signin")
    return render(request,"scheduling/add_slot.html")


#List all the Slots addded by the interviewer 
@login_required
def schedules_list(request):
    schedules = Schedules.objects.filter(uid_id=request.user.uid_id)
    print(schedules)
    
    #if schedules.Slot_time < time_now:
        #delete(schedules)
    return render(request,"scheduling/schedules_list.html",{'all':schedules})

#Deleting The Created Slots By Interviewer By Deleting with reference to id(pk) of the Slot created.
@login_required   
def delete(request, id): 
     dele = Schedules.objects.get(id=id)
     dele.delete()
     return redirect('schedules_list')
 
 
def re(request):
    if request.method == "POST":
        item_id = request.POST.get('slot_id')
        print(item_id)
        ee_id = request.POST.get("ee_id")
        print(ee_id)
        er_name = request.POST.get("er_name")
        print(er_name)
        ee_name = request.POST.get("ee_name")
        print(ee_name)
        er_email = request.POST.get("er_email")
        print(er_email)
        
        subject = "Student Requested for Mock Interview!!"
        email_sub = "Requested Mock Interview by " + ee_name
        message = "Hello" + ' ' + er_name + '!! \n' +'Mock interview Requested by' + ee_name + '\n please check your Account!!\n\n Thanking You\n Team MocX' 
        from_email = settings.EMAIL_HOST_USER
        to_list = [er_email]
        send_mail(subject, message, from_email, to_list, fail_silently=True) #Send mail to the Interviewer!
            
        send_mail( # send one to ourselves when a new time slot is added by the interviewer!!
                        email_sub,
                         "Mock interview is requested by:--"+ee_name+" \n\n "+"For the interviewer:--"+er_name+" \n\n "+"for slot id:--"+item_id,
                         'noreply@mocx.in',
                        ['rishikiranap@gmail.com'] 
                     )
        
        
    return render(request,"scheduling/re.html")
        
