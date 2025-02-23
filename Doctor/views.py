from django.shortcuts import render , redirect
from django.http import HttpResponse
from Appointment.models import *
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings



# Create your views here.


def dummy(request):
    return HttpResponse('Hello doctor')

def doctor_view(request):
    return render (request,'doctor_view.html')

def show_appointment(request):
    id = request.user.id
    doc = Doctor.objects.get(account_id=id)
    status= Status.objects.filter(id=2)
    appointment = Testappointment.objects.filter(doctor_id=doc.id)
    
    for app in appointment:
        
        patient  = Patient.objects.get(id=app.patient_id)
        slot = Testslot.objects.filter(id=app.slot_id)
        
    return render(request,'show_appointment.html',{'doc':doc,'appointment':appointment,'patient':patient,'slot':slot,'status':status})




def confirm_booking(request,id):
    appointment = Testappointment.objects.get(id=id)
    patient = Patient.objects.get(id=appointment.patient_id)

    if request.method=='POST':
        st = request.POST['status']
        appointment.status_id = st
        appointment.save()

    # sending mail to the patient
        
        html_template = 'doctor_availability.html'
        html_message =  render_to_string(html_template)
        subject = 'Appointment Booking Confirmation'
        email_from = settings.EMAIL_HOST_USER
       
        recipient_list=[patient.email]
        message = EmailMessage(subject,html_message,email_from,recipient_list)
        message.content_subtype = 'html'
        message.send()

        messages.success(request,'Details saved successfully')
    return render(request,'show_appointment.html',{'patient':patient})
