from django.shortcuts import render,redirect
from django.http import HttpResponse
from Appointment.models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import random
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import datetime



# Create your views here.
def patient(request):
    return render(request,'homes.html')

def patient_view(request):
    return render(request,'patient_view.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        
        password = request.POST['password']
        # Generating password 
        
        # print ('view1',password)

        # password hashing
        # password = make_password(request.POST['password'])
        hash_password = make_password(password)

        # patient = Patient(name=name,email=email,contact=contact,address=address)
        # patient.save()
        # messages.success(request,'Details saved successfully')
        account = Accounts(email=email,password=hash_password,is_patient=True)
        account.save()
        

        # saving the details in patient model using account id
        create_patient(request,account.pk)
        
    


        # sending login credentials to the patient
        credentials = {'email':email,'password':password,'name':name}
        html_template = 'login_credential.html'
        html_message =  render_to_string(html_template,context=credentials)
        subject = 'Welcome to Medinova Hospitals'
        email_from = settings.EMAIL_HOST_USER
       
        recipient_list=[email]
        message = EmailMessage(subject,html_message,email_from,recipient_list)
        message.content_subtype = 'html'
        message.send()
        messages.success(request,'Details saved successfully')
        return redirect('login')

      
        
    return render(request,'signup.html')



def create_patient(request,account_id):
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        
        patient = Patient(name=name,email=email,contact=contact,address=address,account_id=account_id)
        patient.save()



def doctor_list(request):
    user_id = bool(request.user.is_patient)
    
    # print ('moooney',user_id)
    doc = Doctor.objects.all()
    
    slot = Slots.objects.all()
    
    
        
    return render (request,'doctor_list.html',{'doctor':doc,'slot':slot})

def book_appointment(request,id):
    user_id = request.user.id
    pa = Patient.objects.get(account_id = user_id)
    pi = Doctor.objects.get(pk=id)
    date = Available_dates.objects.filter(doctor_id = id)
    
    
    if request.method == 'POST':
        patient = pa.id
        hospital = request.POST['hospital']
        doctor = pi.id
        date = request.POST['date']
        slots = request.POST['slot']

        appointment = Appointment(patient_id= patient,hospital_id=hospital,doctor_id=doctor,date_id=date,slot_id=slots)
        appointment.save()
        
        booked_slot = Slots.objects.get(id=slots)
        booked_slot.is_active = False
        booked_slot.save()
        

    # getting the slot wrt the slot id provided by patient

        sl  = Slots.objects.get(id=slots)


    # sending mail to patient after booking the appointment
        details = {'date':date , 'slot1':sl.start_time,'slot2':sl.end_time,'name':pa.name}
        html_template = 'booking_confirmation.html'
        html_message =  render_to_string(html_template,context=details)
        subject = 'Appointment Booking Details'
        email_from = settings.EMAIL_HOST_USER
       
        recipient_list=[pa.email]
        message = EmailMessage(subject,html_message,email_from,recipient_list)
        message.content_subtype = 'html'
        message.send()
         
    # sending mail to doctor after booking the appointment

        doctor_html_template = 'doctor_booking_confirmation.html'
        doctor_html_message = render_to_string(doctor_html_template,context=details)
        doctor_recipient_list = [pi.email]
        message2 = EmailMessage(subject,doctor_html_message,email_from,doctor_recipient_list)
        message2.content_subtype = 'html'
        message2.send()

        messages.success(request,'Appointment booked successfully')


    return render(request,'book_appointment.html',{'pi':pi,'pa':pa,'date':date})

# #testing
import datetime as dt


def test_book_appointment(request,id):
    
    user_id = request.user.id
    pa = Patient.objects.get(account_id = user_id)
    pi = Doctor.objects.get(pk=id)
    # start_time = dt.datetime.strptime(str(pi.work_start_time), '%H:%M:%S')
    # end_time = dt.datetime.strptime(str(pi.work_end_time), '%H:%M:%S')
    # time_zero = dt.datetime.strptime('00:00', '%H:%M')
    # gap      = dt.datetime.strptime('00:15','%H:%M')
    
    
    # x=[]
    # y=[]
    # while start_time < end_time  :
        
    #     a =(start_time - time_zero + gap).time()
    #     b = start_time - time_zero + gap

    #     # x.append(start_time.strftime('%H:%M'))
    #     x.append(str(start_time.strftime('%H:%M')))
    #     y.append(b.time())
    #     start_time = b
    # booked_sl = booked_slot(request)
    # print (x)
    # print (booked_sl)
    if request.method == 'POST':
        patient = pa.id
        hospital = request.POST['hospital']
        doctor = pi.id
        date = request.POST['date']
        # print (date)
        slot = request.POST['slot']

        
        # booked_slot(request,date,doctor)
    # z=[]
    # for i in x:
    #     if i not in booked_sl:
    #         z.append(i)
    # print ('raja',z)

        time_zero = dt.datetime.strptime('00:00', '%H:%M')
        gap      = dt.datetime.strptime('00:15','%H:%M')
        slot_end_time =  (dt.datetime.strptime(slot,'%H:%M')-time_zero + gap).time()
        
        book_slot = Testslot(start_time=slot,end_time=str(slot_end_time),date = date ,doctor_id=doctor)
        book_slot.save()
        
        appointment = Testappointment(patient_id= patient,hospital_id=hospital,doctor_id=doctor,date=date,slot_id=book_slot.id,status_id=1)
        appointment.save()
 # getting the slot wrt the slot id provided by patient

        sl  = Testslot.objects.get(id=book_slot.id)


    # sending mail to patient after booking the appointment
        details = {'date':date , 'slot1':sl.start_time,'slot2':sl.end_time,'name':pa.name}
        html_template = 'booking_confirmation.html'
        html_message =  render_to_string(html_template,context=details)
        subject = 'Appointment Booking Details'
        email_from = settings.EMAIL_HOST_USER
       
        recipient_list=[pa.email]
        message = EmailMessage(subject,html_message,email_from,recipient_list)
        message.content_subtype = 'html'
        message.send()
         
    # sending mail to doctor after booking the appointment

        doctor_html_template = 'doctor_booking_confirmation.html'
        doctor_html_message = render_to_string(doctor_html_template,context=details)
        doctor_recipient_list = [pi.email]
        message2 = EmailMessage(subject,doctor_html_message,email_from,doctor_recipient_list)
        message2.content_subtype = 'html'
        message2.send()

        messages.success(request,'Appointment booked successfully')


    return render(request,'test_book_appointment.html',{'pi':pi,'pa':pa})



def get_available_slot(request):
    date = request.GET.get('date')
    doctor = request.GET.get('doctor')
    pi = Doctor.objects.get(id=doctor)
    work_start_time = dt.datetime.strptime(str(pi.work_start_time), '%H:%M:%S')
    work_end_time = dt.datetime.strptime(str(pi.work_end_time), '%H:%M:%S')
    time_zero = dt.datetime.strptime('00:00', '%H:%M')
    gap      = dt.datetime.strptime('00:15','%H:%M')
    
    
    x=[]
    y=[]
    while work_start_time < work_end_time  :
        
        a =(work_start_time - time_zero + gap).time()
        b = work_start_time - time_zero + gap

        # x.append(start_time.strftime('%H:%M'))
        x.append(str(work_start_time.strftime('%H:%M')))

        y.append(b.time())
        work_start_time = b
    print ('rani',x)
    # filtering booked slots
    booked_sl = Testslot.objects.filter(date = date,doctor_id=doctor)
    z = []
    for i in booked_sl:
        z.append(i.start_time)
    print('raja',z)
    a=[]
    for i in x:
        if i not in z:
            a.append(i)
    print(a)
    return render(request,'test_load_slot.html',{'z':a})
# def booked_slot(request,date,doctor):
    
    
#     booked_slot = Testslot.objects.filter(date=date,doctor_id=doctor)
#     l=[]
#     for i in booked_slot:
#         l.append(i.start_time)
#     return (l)
    
    
#end



def load_slot(request):
    
    date_id=request.GET.get('date')
    slot = Slots.objects.filter(dates_id=date_id,is_active=True)
    return render(request,'load_slot.html',{'slots':slot})


# def my_booking(request):
    
#     user = request.user.id
#     patient = Patient.objects.get(account_id=user)
#     appointment = Appointment.objects.filter(patient_id=patient.id)
    
#     for app in appointment:
#         slot = Slots.objects.filter(id=app.slot_id)
#         date = Available_dates.objects.filter(id=app.date_id)
       
        
#     return render(request,'my_booking.html',{'appointment':appointment,'d':slot,'date':date})



def my_booking(request):
    
    user = request.user.id
    patient = Patient.objects.get(account_id=user)
    appointment = Testappointment.objects.filter(patient_id=patient.id)
    
    for app in appointment:
        slot = Testslot.objects.filter(id=app.slot_id)
       
        
    return render(request,'my_booking.html',{'appointment':appointment,'d':slot})


def load_doctor(request):
    hospital_id = request.GET.get('hospital')
    doctor = Doctor.objects.filter(hospital_id=hospital_id).order_by('name')
    return render(request,'load_doctor.html',{'doctor':doctor})














    