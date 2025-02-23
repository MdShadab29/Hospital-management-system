
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.template import loader
from django.shortcuts import redirect
from .forms import *
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
import random
import datetime as dt



def home(request):
    return render(request,'home.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request,email=email,password=password)
        # print ('view2',user)        
        if user is not None and user.is_admin:
            login(request,user)
          
            return redirect ('admin_view')
        elif user is not None and user.is_doctor:
            login(request,user)
            return redirect('doctor_view')
        elif user is not None and user.is_patient:
            login(request,user)
            return redirect('patient_view')
        else:
            
            return render (request,'login.html')
           
        
    else:
         return render(request,'login.html')
    
   
def admin_view(request):
    return render(request,'admin_view.html')


def log_out(request):
    logout (request)
    return render (request,'login.html')



def hospital(request):
    hos = Hospital.objects.all
    return render (request,'hospitals.html',{'hos':hos})


def add_hospital(request):
    if request.method == "POST":
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        work_start_time= request.POST['work_start_time']
        work_end_time = request.POST['work_end_time']

        # Checking whether hospital already exists

        if Hospital.objects.filter(name=name).exists():
            messages.info(request,'This hospital is already registered with us')
            return redirect('addhospital')

        hospital = Hospital(name=name,contact=contact,address=address,work_start_time=work_start_time,work_end_time=work_end_time)
        hospital.save()
        messages.success(request,'Hospital added successfully')
        return redirect('hospital')

    return render (request,'add_hospital.html')
    # return redirect('hospital')



def edit_hos(request,id):
    displayhos = Hospital.objects.get(id=id)
    return render(request,'edit_hospital.html',{'hospital':displayhos})



def update_hos(request,id):
    if request.method == 'POST':
        pi = Hospital.objects.get(pk=id)
        form = Updatehos(request.POST,instance=pi)
        form.is_valid()
        form.save()
        messages.success(request,"Hospital updtaed successfully")
        return redirect('hospital')
    else:
        pi = Hospital.objects.get(pk=id)
        form = Updatehos(instance=pi)
    return render (request ,'edit_hospital.html',{'form':form})




def delete_hospital(request,id):
    if request.method == 'POST':
        pi = Hospital.objects.get(pk=id)
        pi.delete()
        messages.success(request,"Hospital deleted successfully")
        return redirect('hospital')




def doctor(request):
    doc = Doctor.objects.all
    return render (request,'doctor.html',{'doc':doc})




def add_doctor(request):
    
    hospital = Hospital.objects.all()

    h = {'hospital':hospital}
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        hospital_id = request.POST['hospital']
        speciality = request.POST['speciality']
        address = request.POST['address']
        work_start_time= request.POST['work_start_time']
        work_end_time = request.POST['work_end_time']
        char = list('0123456789')
        lenght = 6
        password = ''
        for i in range (lenght):
            password += random.choice(char)
        print ('test',password)

        # password hashing
        hash_password = make_password(password)


        # Checking whether doctor already exists

        if Doctor.objects.filter(email=email).exists():
            messages.info(request,'This email is already registered')
            return redirect('add_doctor')

        
        # Saving credentials in Account model 

        account = Accounts(email=email,password=hash_password,is_doctor = True)
        account.save()
        

        # saving the details in doctor model using account id
        
        create_doctor(request,account.id)
        

        
        # sending mail

        credentials = {'email':email,'password':password}
        html_template = 'register_doctor.html'
        html_message =  render_to_string(html_template,context=credentials)
        subject = 'Welcome to Medinova Hospitals'
        email_from = settings.EMAIL_HOST_USER
       
        recipient_list=[email]
        message = EmailMessage(subject,html_message,email_from,recipient_list)
        message.content_subtype = 'html'
        message.send()
        messages.success(request,'Doctor added successfully')
        return redirect('doctor')
    
    return render (request,'add_doctor.html',h)


def create_doctor(request,account_id):
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        hospital_id = request.POST['hospital']
        speciality = request.POST['speciality']
        address = request.POST['address']
        work_start_time= request.POST['work_start_time']
        work_end_time = request.POST['work_end_time']
        
        doctor = Doctor(name=name,email=email,hospital_id=hospital_id,address=address,speciality=speciality,work_start_time=work_start_time,work_end_time=work_end_time,account_id=account_id)
        doctor.save()
        # save_date(request,doctor.id)
        # slot(request,doctor.id)
        
        



import datetime 
from datetime import timedelta 

# Saving dates

def save_date(request,doctor_id):
    current_date = datetime.date.today()
# print (current_date)
    while current_date < (datetime.date.today()+timedelta(31)):
        available_date = Available_dates(available_dates=current_date,doctor_id=doctor_id)
        available_date.save()
        # slot(request,doctor_id,available_date.id)
        current_date = current_date+timedelta(1)


# Saving slots

def slot(request,doctor_id,dates_id):
    if request.method == 'POST':
        work_start_time= request.POST['work_start_time']
        work_end_time = request.POST['work_end_time']

        start_time = dt.datetime.strptime(str(work_start_time), '%H:%M')
        end_time = dt.datetime.strptime(str(work_end_time), '%H:%M')
        time_zero = dt.datetime.strptime('00:00', '%H:%M')
        gap      = dt.datetime.strptime('00:15','%H:%M')
        while start_time < end_time  :
            a = (start_time - time_zero + gap).time()
            b = start_time - time_zero + gap
            # print ('raja',a)            
            slot = Slots(start_time = start_time , end_time=a,doctor_id=doctor_id,dates_id=dates_id)
            slot.save()
            start_time = b
        
            





def edit_doc(request,id):
    hospital = Hospital.objects.all
    displaydoc = Doctor.objects.get(id=id)
    return render (request,'edit_doctor.html',{'doctor':displaydoc,'hospital':hospital})


def update_doc(request,id):
    if request.method == 'POST':
        pi = Doctor.objects.get(pk=id)
        form = Updatedoc(request.POST,instance=pi)
        form.is_valid()
        form.save()
        messages.success(request,"Doctor updated successfully")
        return redirect('doctor')
    else:
        pi = Doctor.objects.get(pk=id)
        form = Updatedoc(instance=pi)
    return render (request ,'edit_doctor.html',{'form':form})




def delete_doctor(request,id):
    if request.method == 'POST':
        pi = Doctor.objects.get(pk=id)
        pi.delete()
        messages.success(request,"Doctor deleted successfully")
        return redirect('doctor')



def about(request):
    return render(request,'about.html')



def appointments(request):
    
    app = Appointment.objects.all()
    return render (request,'appointments.html',{'app':app})
    
# def load_slot(request):
#     date=request.GET.get('date')
#     slot = Slots.objects.filter(date=date).order_by('name')
#     return render(request,'slot.html',{'slot':slot})





