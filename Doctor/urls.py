from django.urls import path
from Doctor.views import *


urlpatterns = [
    path('',dummy,name='dummy'),
    path('doctor_view/',doctor_view,name='doctor_view'),
    path('show_appointment',show_appointment,name='show_appointment'),
    
    path('confirm_booking/<int:id>',confirm_booking,name='confirm_booking')
]