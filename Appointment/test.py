      
    
import datetime as dt



start_time = dt.datetime.strptime('10:00', '%H:%M')
end_time = dt.datetime.strptime('12:00', '%H:%M')
time_zero = dt.datetime.strptime('00:00', '%H:%M')
gap      = dt.datetime.strptime('00:15','%H:%M')
while start_time < end_time  :
    a = (start_time - time_zero + gap).time()
    b = start_time - time_zero + gap
    print (start_time)            
    
    start_time = b



l=[]
print (type(l))