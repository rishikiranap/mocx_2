from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class manager(BaseUserManager):
    def create_user(self, email, username, password, first_name, last_name, phone):
        if not email:
            raise ValueError("users must have an email address")

        if not username:
                raise ValueError('users must have an username')

        if not phone:
            raise ValueError('users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )    
        user.set_password(password)
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

class Account(AbstractBaseUser):
    email = models.EmailField( max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, default="none")
    last_name = models.CharField(max_length=30 , default="none")
    first_name = models.CharField(max_length=30 , default="none")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username','first_name','last_name','phone']
    
    objects = manager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True






        


            



    