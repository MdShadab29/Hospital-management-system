from django.contrib import admin
from django.urls import path,include
from Patient.views import *
urlpatterns = [
    # path('',patient,name='patient'),
    path('signup/',signup,name='signup'),
    path('load_doctor/',load_doctor,name='load_doctor'),
    path('patient_view/',patient_view,name='patient_view'),
    path('doctor_list/',doctor_list,name='doctor_list'),
    path('book_appointment/<int:id>/',book_appointment,name='book_appointment'),
    path('test_book_appointment/<int:id>/',test_book_appointment,name='test_book_appointment'),

    path('my_booking/',my_booking,name='my_booking'),
    path('load-slot/',load_slot,name='ajax_load_slot'),
    path('test-load-slot',get_available_slot,name='ajax_load_available_slot')
]