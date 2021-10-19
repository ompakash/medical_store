from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Patient, Doctor
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage


# Create your views here.

def home(request):
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

    return render(request, template_name='store/patient.html')


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
            user = User(username=username,first_name=firstname, last_name=lastname,email=email)
            user.set_password(password)                         
            user.save()

            doctor = Doctor.objects.create(user=user,image=url,address=address,city=city,state=state,pincode=pincode)

            messages.info(request, "Account Created Successfully")
            return redirect('/')

    return render(request, template_name='store/doctor.html')


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



def profile(request):
    # print(request.user)
    user_type = request.session['user_type']
    if user_type == "doctor":        
        user_profile = Doctor.objects.get(user=request.user)
        print(user_profile.image)

    if user_type == "patient":
        user_profile = Patient.objects.get(user=request.user)

    
    
    context = {'user_profile': user_profile}

    return render(request, 'store/profile.html', context)