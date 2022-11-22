from django.db import models
from accounts.models import InterviewerAccount,IntervieweeAccount

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
        return str(self.Slot_time)
    
    
    
    
    
    
class Scheduled(models.Model):
    STATUS = [
        ("C","Confirmed"),
        ("D","Declined"),
    ]
    Student_uid = models.ForeignKey(IntervieweeAccount, on_delete=models.CASCADE)
    Interviewer_Slot = models.OneToOneField(Schedules, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS, default="None")
    
    def change_to_confirmed(self):
        self.status = "C"
        self.save()

    
    def change_to_declined(self):
        self.status = "D"
        self.save()
        
    def __str__(self):
        return self.status
    