from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


class manager(BaseUserManager):
    def create_user(self, email, username, password, **kwargs):
        
        if not kwargs:
            phone=None
            first_name= None
            last_name = None

        user = self.model(
        email=self.normalize_email(email),
        username=username,
        password=password,
        phone=phone,
        last_name=last_name,
        first_name=first_name,
        ) 
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_interviewee(self, Occupation, Company, Institute_name, **kwargs):
        
        if not kwargs:
            Residence=None
            Res_city=None
            Year_of_study=None

        user = self.model(
        Occupation=Occupation,
        Company=Company,
        Institute_name=Institute_name,
        Year_of_study=Year_of_study,
        Residence=Residence,
        Res_city=Res_city,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class BasicAccount(AbstractBaseUser, PermissionsMixin):
    uid=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField( max_length=60, unique=True)
    username = models.CharField(max_length=60, unique=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone = models.CharField(max_length=13, blank=True, null=True)
    last_name = models.CharField(max_length=30,blank=True, null=True)
    first_name = models.CharField(max_length=30,blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    objects = manager()

    def __str__(self):
        return (self.email) 
    
    
class IntervieweeAccount(models.Model):
    uid = models.OneToOneField(BasicAccount, on_delete=models.CASCADE, primary_key=True)

    Occupation = models.CharField(max_length=60, default="empty", blank=True, null=True)
    Company = models.CharField(max_length=60, default="empty", blank=True, null=True)
    Institute_name = models.CharField(max_length=60, default="empty", blank=True, null=True)
    state = models.CharField(max_length=40, default="empty", blank=True, null=True)
    city = models.CharField(max_length=40, default="empty", blank=True, null=True)
    Year_of_study = models.CharField(max_length=60, default="empty", blank=True, null=True)
    Residence = models.CharField(max_length=60, default="empty", blank=True, null=True)
    Res_city = models.CharField(max_length=60, default="empty", blank=True, null=True)
    
    objects = manager()
    
    def __str__(self):
        return self.Occupation
    
    
class InterviewerAccount(models.Model):
    pass
    
    
    






        


            



    