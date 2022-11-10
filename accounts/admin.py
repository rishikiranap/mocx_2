from django.contrib import admin
from .models import BasicAccount, IntervieweeAccount, InterviewerAccount

# Register your models here.
admin.site.register(BasicAccount)
admin.site.register(IntervieweeAccount)
admin.site.register(InterviewerAccount)


