from django.shortcuts import render, redirect
import pytz
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.models import InterviewerAccount,BasicAccount
from .models import Schedules
from accounts.backend import EmailBackend
from mocx_2 import settings
from django.core.mail import send_mail


# Create your views here.
#adding mock interview's time slots by the interviewer
@login_required
def add_slot(request):
    if request.method == 'POST':
       
        Slot = request.POST['Slot_TimeDate']
        #Getting Uid from InterviewerAccount linked with BasicAccount
        interviewer = InterviewerAccount.objects.get(uid = request.user)
        add_slot = Schedules(uid = interviewer)
        add_slot.Slot_time = Slot
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
    schedules = Schedules.objects.all
    return render(request,"scheduling/schedules_list.html",{'all':schedules})

#Deleting The Created Slots By Interviewer By Deleting with reference to id(pk) of the Slot created.
@login_required   
def delete(request, id): 
     dele = Schedules.objects.get(id=id)
     dele.delete()
     return redirect('schedules_list')
