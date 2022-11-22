from django.contrib.auth.backends import ModelBackend
from .models import BasicAccount

class EmailBackend(ModelBackend):
    def authenticate(email, password, **kwargs):
      email = email
      password = password
       
      user = BasicAccount.objects.get(email=email)
      try:
         if user.check_password(password) is True:
            return user
      except:
         print("not working!")
         

