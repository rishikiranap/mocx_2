from django.db import models
from accounts.models import InterviewerAccount,IntervieweeAccount
from datetime import datetime
# Create your models here.


class Schedules(models.Model):
    
    STATUS = [
        ("E","Empty"),
        ('A',"Added"),
        ('D',"Declined"),
    ]
    uid = models.ForeignKey(InterviewerAccount, on_delete=models.CASCADE)
    Slot_time = models.DateTimeField(blank=False)
    Slot_status = models.CharField(max_length=1, choices=STATUS, default="E")
    
    def change_to_added(self):
        self.Slot_status = "A"
        self.save()
        
    def change_to_empty(self):
        self.Slot_status = "E"
        self.save()
    
    def change_to_declined(self):
        self.Slot_status = "D"
        self.save()
        
    def __str__(self):
        return str(self.Slot_time.strftime(("%d-%m-%Y at %H:%M")))
    
    
    
    
    
    
class Scheduled(models.Model):
    PAYMENT =[
        ("S","Successful"),
        ("P","Pending"),
        ("D","Declined"),
        
    ]
    Student_uid = models.ForeignKey(IntervieweeAccount, on_delete=models.CASCADE)
    Interviewer_Slot = models.OneToOneField(Schedules, on_delete=models.CASCADE)
    Payment = models.CharField(max_length=1, choices=PAYMENT, default="P")
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100,null=True,blank=True)
      
      
    def change_to_Successful(self):
        self.Payment = "S"
        self.save()

    
    def change_to_declined(self):
        self.Payment = "D"
        self.save()
        
    def __str__(self):
        return self.Payment
    