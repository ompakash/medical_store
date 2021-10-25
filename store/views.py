from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import *
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


# Original answer said:
from django.templatetags.static import static
# Improved answer (thanks @Kenial, see below)
# from django.contrib.staticfiles.templatetags.staticfiles import static

# url now contains '/static/x.jpg', assuming a static path of '/static/'


# import datetime

from datetime import datetime,timedelta


# import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import os

# from google_auth_oauthlib.flow import Flow, InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# from google.auth.transport.requests import Request
# import pytz
# from google.oauth2 import service_account

# import os

# from store.google_cal import get_calendar_service

# Create your views here.


def cred():
    credentials =    {
    "installed": {
        "client_id": "1002660884057-r908c8n3t3eu870vn58uk91gcfivu7ci.apps.googleusercontent.com",
        "project_id": "quickstart-330016",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [
            "urn:ietf:wg:oauth:2.0:oob",
            "http://localhost"
        ]
    }
}
    credentials1 = json.dumps(credentials)
    print(credentials1)

    return credentials1



def home(request):
    
 
    # get_calendar_service()

    return render(request, template_name="store/home.html")


def patient(request):

    if request.method == "POST":
        
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        image= request.FILES['image']

        fs = FileSystemStorage()
        filename = fs.save(image.name, image) # Storing image in database with auto generated name:
        url = fs.url(filename)

  

        if User.objects.filter(email=email).exists():
            messages.error(request, "Sorry E-mail is taken")
            return redirect('patient')

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Sorry Username is taken")
            return redirect('patient')

        elif password != confirmpassword:
            messages.error(request,"Password and Confirm password didn't match")
            return redirect('patient')

        else:
            user = User(username=username,first_name=firstname, last_name=lastname,email=email)
            user.set_password(password)                         
            user.save()

            patient = Patient.objects.create(user=user,image=url,address=address,city=city,state=state,pincode=pincode)

            messages.info(request, "Account Created Successfully")
            return redirect('/')


    return render(request, 'store/patient.html')


def doctor(request):
    if request.method == "POST":
        
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        image= request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(image.name, image) # Storing image in database with auto generated name:
        url = fs.url(filename)
 

        if User.objects.filter(email=email).exists():
            messages.error(request, "Sorry E-mail is taken")
            return redirect('patient')

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Sorry Username is taken")
            return redirect('patient')

        elif password != confirmpassword:
            messages.error(request,"Password and Confirm password didn't match")
            return redirect('patient')

        else:
            user = User(username=username,first_name=firstname, last_name=lastname,email=email,is_staff=True)
            user.set_password(password)                         
            user.save()

            doctor = Doctor.objects.create(user=user,firstname=firstname,lastname = lastname,image=url,address=address,city=city,state=state,pincode=pincode)

            messages.info(request, "Account Created Successfully")
            return redirect('/')
            

    return render(request, 'store/doctor.html')


def logout_page(request):
    logout(request)
    messages.info(request,"You Logged Out")
    return redirect('/')


def login_page(request):
    if request.method == 'POST':
        is_doctor = request.POST.get('doctor')
        is_patient = request.POST.get('patient')
        login_username = request.POST['usernameL']
        login_password = request.POST['passwordL']
        # print(is_doctor)

        try:
            if is_doctor=='doctor':

                user = authenticate(username = login_username,password = login_password)

                if user:
                    login(request, user)
                    request.session['user_type'] = is_doctor
                    messages.info(request,'You are Logged In')
                    return redirect('/profile')
                
                else:
                    messages.warning(request, 'Invalid Credentials')
                    return redirect('/login')

            if is_patient=='patient':

                user = authenticate(username = login_username,password = login_password)

                if user:
                    request.session['user_type'] = is_patient
                    login(request, user)
                    messages.info(request,'You are Logged In')
                    return redirect('/profile')
                
                else:
                    messages.warning(request, 'Invalid Credentials')
                    return redirect('/login')


        except Exception as e:
            messages.warning(request,'INVALID CREDENTIALS')
            messages.info(request,f'An Error Occured {e}')
            return redirect('/')

    return render(request, template_name='store/login.html')


@login_required
def profile(request):
    # print(request.user)
    user_type = request.session['user_type']
    if user_type == "doctor":        
        user_type = 'doctor'
        user_profile = Doctor.objects.get(user=request.user)
        # print(user_profile.image)

    if user_type == "patient":
        user_type = 'patient'
        user_profile = Patient.objects.get(user=request.user)

    
    
    context = {'user_profile': user_profile}
    print(user_type)

    return render(request, 'store/profile.html', context)



@login_required
def bloghome(request):

    mentalhealth = Blogpost.objects.filter(category='mentalhealth')
    heartdisease = Blogpost.objects.filter(category='heartdisease')
    covid19 = Blogpost.objects.filter(category='covid19')
    immunization = Blogpost.objects.filter(category='immunization')

    mh_list=[]
    for mh in mentalhealth:
        if mh.draft == False:
            mh_list.append(mh)

    hd_list=[]
    for hd in heartdisease:
        if hd.draft == False:
            hd_list.append(hd)
    
    cd_list = []
    for cd in covid19:
        if cd.draft == False:
            cd_list.append(cd)
    
    im_list = []
    for im in immunization:
        if im.draft == False:
            im_list.append(im)

    context = { 'mentalhealth':mh_list, 'heartdisease':hd_list, 'covid19':cd_list, 'immunization':im_list }
    # print(covid19)
    
    return render(request,'blog/bloghome.html',context)


@login_required
def newpost(request):
    if request.method == "POST":
        author = request.POST.get('author')
        title = request.POST.get('title')
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        is_draft = request.POST.get("is_draft")

        # IMAGE
        image= request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(image.name, image) # Storing image in database with auto generated name:
        url = fs.url(filename)

        user = User.objects.get(username=author)
        writer = Doctor.objects.get(user=user)


        if is_draft == 'on':
            draft = True
        else:
            draft = False

        Blogpost.objects.create(author=writer, title=title, image=url, category=category, summary=summary, content=content, draft=draft)

        messages.success(request, 'The post have been uploaded successfully.')
        return redirect('/mypost')

        
    user_type = request.session['user_type']
    if user_type == "patient":
        # user_profile = Patient.objects.get(user=request.user)
        messages.warning(request, "Sorry Patient can't create a post")
        return redirect('/bloghome')
    
    return render(request, template_name='blog/newpost.html')


@login_required
def mypost(request):

    # user = User.objects.filter(username=request.user).last()
    # author = Doctor.objects.filter(user=user).last()

    user = User.objects.get(username=request.user)
    author = Doctor.objects.get(user=user)
    mypost = Blogpost.objects.filter(author=author)
    
    # print(user,author,mypost)

    user_type = request.session['user_type']
    if user_type == "patient":
        user_profile = Patient.objects.get(user=request.user)
        messages.warning(request, "Sorry Patient can't open MY POST")
        return redirect('/bloghome')

    context = {'mypost':mypost}
    
    return render(request, 'blog/mypost.html',context)

@login_required
def postview(request,id):
    post = Blogpost.objects.get(id=id)

    return render(request, 'blog/postview.html',{'post':post})


@login_required
def updatepost(request,id):
    post = Blogpost.objects.get(id=id)
    # print(post)

    if request.method == "POST":
        # print(post.id)
        # postId = request.POST.get("postId")
        title = request.POST.get("title")
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        is_draft = request.POST.get("is_draft")

        post = Blogpost.objects.get(id=post.id)
    
        try:
            image= request.FILES['image']
        
            fs = FileSystemStorage()
            filename = fs.save(image.name, image) # Storing image in database with auto generated name:
            url = fs.url(filename)
        except Exception as e:
            url = post.image

        if summary == "":
            summary = post.summary

        if content == "":
            content = post.content

        if is_draft == 'on':
            draft = True
        else:
            draft = False

        # print(post.title,post.image,post.categorsy,post.summary,post.content,post.draft)
        post.title = title
        post.image = url
        post.category = category
        post.summary = summary
        post.content = content
        post.draft = draft
        post.save()
        # print(post.title,post.image,post.category,post.summary,post.content,post.draft)
        messages.success(request, 'The post have been updated successfully.')
        return redirect('/mypost')

    return render(request, 'blog/updatepost.html',{'post':post})


@login_required
def doctorlist(request):
    doctors = Doctor.objects.all()
    # print(doctors)
    
    # appointment = Appointment.objects.filter(id=1).first()1
    context = {'doctors':doctors}
    return render(request, 'appointment/doctorlist.html',context)


@login_required
def appointment_form(request,id):
    if request.method == "POST":

        speciality = request.POST.get('speciality')
        appointmentdatetime = request.POST.get('appointmentdatetime')

        doctor = Doctor.objects.filter(id=id).first()
        print(doctor,speciality,appointmentdatetime)

        appointment = Appointment(doctor=doctor,required_speciality=speciality,datetime_of_appointment=appointmentdatetime)

        appointment.save()
        # print(appointment.datetime_of_appointment.time())
        # print(appointment.datetime_of_appointment.time)
        # print(appointment.datetime_of_appointment)
        

        

        request.session['doctor_id'] = doctor.id
        request.session['appointment_id'] = appointment.id
        messages.success(request, 'The appointment have been scheduled successfully.')
        # print(doctor.id)
        # print(appointment.id)

        return redirect('/appointmentdetails')

    return render(request, 'appointment/appointment_form.html')



@login_required
def appointmentdetails(request):


    doctor_id = request.session['doctor_id']     
    appointment_id = request.session['appointment_id']     
    doctor = Doctor.objects.filter(id=doctor_id).first()
    appointment = Appointment.objects.filter(id=appointment_id).first()
    # start_time_of_appointment = str(appointment.start_time)
    # end_time_of_appointment = sumTime(str(appointment.start_time), '00:45:00')
    date_of_appointment = appointment.datetime_of_appointment.date
    start_time = f"{appointment.datetime_of_appointment.hour}:{appointment.datetime_of_appointment.minute}:00"
    # print("START TIME ",start_time)
    end_time = sumTime(str(start_time), '00:45:00')
    # print("END TIME ",end_time)


    context = {'doctor': doctor, 'appointment': appointment,'start_time':start_time,'end_time':end_time,'date_of_appointment':date_of_appointment}


    try:
        get_calendar_service()
        # maine(doctor, speciality, start_time, end_time)
    except Exception as e:
        print(e)

    # print(appointment.datetime_of_appointment)
    # print(appointment.datetime_of_appointment.timestamp())
    # print(appointment.datetime_of_appointment.hour)
    # print(appointment.datetime_of_appointment.minute)


    return render(request, 'appointment/appointmentdetails.html', context)

    return render(request, 'appointment/appointmentdetails.html')

def sumTime(t1, t2):
    timeList = [t1, t2]
    mysum = timedelta() 
    for i in timeList:
        (h, m, s) = i.split(':')
        d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        mysum += d
    return str(mysum)




# GOOOGLE CALENDAR


# import datetime
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# CREDENTIALS_FILE = cred()


import json

# json_data = open('/static/store/credentials.json')   
# print('json',json_data)
# data1 = json.load(json_data) # deserialises it
# print('json1',data1)
# data2 = json.dumps(data1) # json formatted string
# print('json2',data2)

# json_data.close()


def get_calendar_service():
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   print("all done...")
   return service

# get_calendar_service()


# # CREATE EVENT

# # from datetime import datetime, timedelta
# # from cal_setup import get_calendar_service


# def maine(doctor,speciality,start_time,end_time):
#    # creates one hour event tomorrow 10 AM IST
#    service = get_calendar_service()
#    print(doctor,speciality,appointmentdate,appointmenttime)
# #    d = datetime.now().date()
# #    tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=2)
# #    start = tomorrow.isoformat()
# #    end = (tomorrow + timedelta(minutes=45)).isoformat()

#    start = start_time 
#    end = end_time

#    event_result = service.events().insert(calendarId='primary',
#        body={
#            "summary": doctor,
#            "description": speciality,
#            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
#            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
#        }
#    ).execute()

#    print("created event")
#    print("id: ", event_result['id'])
#    print("summary: ", event_result['summary'])
#    print("starts at: ", event_result['start']['dateTime'])
#    print("ends at: ", event_result['end']['dateTime'])

# # if __name__ == '__main__':
# #    main()