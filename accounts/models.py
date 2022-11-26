from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
import uuid




class manager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        
        if not kwargs:
            phone=None
            first_name= None
            last_name = None
            is_interviewer = None

        user = self.model(
        email=self.normalize_email(email),
       
        password=password,
        phone=phone,
        last_name=last_name,
        first_name=first_name,
        is_interviewer=is_interviewer,
        ) 
        user.set_password(password)
        user.save(using=self._db)
        return user
            

    def create_superuser(self, email, password):
        user=self.create_user(
            email=self.normalize_email(email),
            
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class BasicAccount(AbstractBaseUser, PermissionsMixin):
    uid_id=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField( max_length=60,unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone = models.CharField(max_length=13, blank=True, null=True)
    last_name = models.CharField(max_length=30,blank=True, null=True)
    first_name = models.CharField(max_length=30,blank=True, null=True, unique=True)
    is_interviewer = models.BooleanField(default=False,blank=True,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [' ']
    
    objects = manager()

    def __str__(self):
        return (self.email) 
    
    
OCCUPATION=(
    ('STUDENT', 'STUDENT'),
    ('JOB', 'JOB')
)
    
class IntervieweeAccount(models.Model):
    
    #Connecting Basic-Account Table with Interviewee-Account
     
    uid = models.OneToOneField(BasicAccount, on_delete=models.CASCADE, primary_key=True)
    
    #Other fields in Interviewee-Account
    Occupation = models.CharField(max_length=60, blank=True, null=True, choices=OCCUPATION)
    Company = models.CharField(max_length=60)
    Institute_name = models.CharField(max_length=60, blank=True, null=True)
    State = models.CharField(max_length=40, blank=True, null=True)
    City = models.CharField(max_length=40, blank=True, null=True)
    Year_of_study = models.CharField(max_length=60, blank=True, null=True)
    Residence = models.CharField(max_length=60, blank=True, null=True)
    Res_city = models.CharField(max_length=60, blank=True, null=True)


    def __str__(self):
        return self.Occupation
    
    
class InterviewerAccount(models.Model):
    
    uid = models.OneToOneField(BasicAccount, on_delete=models.CASCADE, primary_key=True)
    Age = models.CharField(max_length=10, null=True, blank=True)
    Experience = models.CharField(max_length=40, null=True, blank=True)
    Price = models.CharField(max_length=30, null=True, blank=True)
    About_me = models.CharField(max_length=200, null=True, blank=True)
    Linkedin = models.URLField(max_length=60, blank=True)
    profile_image = models.ImageField(upload_to='pics', default='dafault.svg')

   
    
    def __str__(self):
        return str(self.Experience)
    
    
    

    
    
    






        


            



    