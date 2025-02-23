from django.urls import path,include
from .views import *
urlpatterns = [
    
    path("",home,name='home'),
    path('login/',user_login,name='login'),
    path('login/',log_out,name='logout'),

    #paths for hospital

    path('addhospital',add_hospital,name='addhospital'),
    path('hospital/',hospital,name='hospital'),
    path('deletehospital/<int:id>/',delete_hospital,name='deletehos'),
    path('edit/<int:id>/',edit_hos,name='edithos'),
    path('update/<int:id>/',update_hos,name='update'),
    path('admin_view/',admin_view,name='admin_view'),
   
    #paths for doctor
    path('doctor/',doctor,name='doctor'),
    path('add_doctor/',add_doctor,name='add_doctor'),
    path('deletedoctor/<int:id>/',delete_doctor,name='deletedoc'),
    path('editdoc/<int:id>/',edit_doc,name='editdoc'),
    path('updatedoc/<int:id>/',update_doc,name='updatedoc'),

    path('about/',about,name='about'),
    path('appointment/',appointments,name='appointment'),
    # path('ajax/load-slot/',load_slot,name='ajax_load_slot'),

    
]