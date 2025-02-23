from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager, User
from django.db import models



# Create your models here.
class Hospital(models.Model):
    name            = models.CharField(max_length=50)
    address         = models.CharField(max_length =100)
    # contact         = models.IntegerField()
    contact         = models.BigIntegerField()
    work_start_time = models.TimeField(default=None,blank=True)
    work_end_time   = models.TimeField(default=None,blank=True)
    created_at      = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at      = models.DateTimeField(auto_now=True,blank=True,null=True)
 
    def __str__(self):
        return self.name



class Status(models.Model):
    name        = models.CharField(max_length=50)
    created_at  = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at  = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name





class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
       
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        
        user = self.create_user(
            email,
            password=password,
           
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    


class Accounts(AbstractBaseUser):
    email = models.EmailField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)


    objects = MyUserManager()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        
        return True

    def has_module_perms(self, app_label):
       
        return True

    @property
    def is_staff(self):
       
        return self.is_admin

    


class Patient(models.Model):
    name        = models.CharField(max_length = 50)
    email       = models.CharField(max_length = 50)
    account     = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    contact     = models.BigIntegerField()
    address     = models.CharField(max_length = 100,default=False)
    created_at  = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at  = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name



class Doctor(models.Model):
    name            = models.CharField(max_length=50)
    email           = models.CharField(max_length=50)
    speciality      = models.CharField(max_length=50)
    address         = models.CharField(max_length=50)
    account         = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    work_start_time = models.TimeField(default=None,blank=True)
    work_end_time   = models.TimeField(default=None,blank=True)
    hospital        = models.ForeignKey(Hospital,on_delete=models.SET_NULL , null=True)
    created_at      = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at      = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    name        = models.CharField(max_length = 50)
    email       = models.CharField(max_length = 50)
    account     = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)    
    created_at  = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at  = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name

class Available_dates(models.Model):
    available_dates = models.DateField(auto_now=False,auto_now_add=False)
    doctor          = models.ForeignKey(Doctor,on_delete=models.CASCADE,default=None)
    


class Slots(models.Model):
    doctor      =   models.ForeignKey(Doctor,on_delete=models.CASCADE)
    dates       =   models.ForeignKey(Available_dates,on_delete=models.CASCADE,default=None)
    start_time  =   models.TimeField(default=None)
    end_time    =   models.TimeField(default=None)
    is_active   =   models.BooleanField(default=True)

#tetsing
class Testslot(models.Model):
    start_time  =   models.CharField(max_length=50)
    end_time    =   models.CharField(max_length=50)
    date        =   models.DateField(auto_now=False,auto_now_add=False,default=None)
    doctor      =   models.ForeignKey(Doctor,on_delete=models.CASCADE,default=None)


class Testappointment(models.Model):
    patient     = models.ForeignKey(Patient,on_delete = models.SET_NULL , null=True)  
    hospital    = models.ForeignKey(Hospital,on_delete = models.SET_NULL , null=True)
    doctor      = models.ForeignKey(Doctor,on_delete = models.SET_NULL , null=True)
    date        = models.DateField(auto_now=False,auto_now_add=False)
    slot        = models.ForeignKey(Testslot,on_delete=models.CASCADE,null=True)
    status      = models.ForeignKey(Status,on_delete = models.SET_NULL , null=True)
    created_at  = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at  = models.DateTimeField(auto_now=True,blank=True,null=True)
#end

class Appointment(models.Model):
    patient     = models.ForeignKey(Patient,on_delete = models.SET_NULL , null=True)  
    hospital    = models.ForeignKey(Hospital,on_delete = models.SET_NULL , null=True)
    doctor      = models.ForeignKey(Doctor,on_delete = models.SET_NULL , null=True)
    date        = models.ForeignKey(Available_dates,on_delete=models.CASCADE,default=None)
    slot        = models.ForeignKey(Slots,on_delete=models.CASCADE,null=True)
    status      = models.ForeignKey(Status,on_delete = models.SET_NULL , null=True)
    created_at  = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at  = models.DateTimeField(auto_now=True,blank=True,null=True)



