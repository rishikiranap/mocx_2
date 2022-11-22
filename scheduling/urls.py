from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
       path('add_slot', views.add_slot, name="add_slot"),
       path('schedules_list', views.schedules_list, name="schedules_list"),
       path('delete/<int:id>', views.delete, name="delete"),
]
