from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('', views.home, name="home"),
   path('signup',views.signup,name="signup"),
   path('IntervieweeReg',views.IntervieweeReg,name="IntervieweeReg"),
   path('InterviewerReg1',views.InterviewerReg1, name='InterviewerReg1'),
   path('InterviewerReg2',views.InterviewerReg2, name='InterviewerReg2'),
   path('signin',views.signin, name="signin"),
   path('signout',views.signout, name="signout"),

]