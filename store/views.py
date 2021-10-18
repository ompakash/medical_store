from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Patient,Doctor
from django.contrib.auth import authenticate, login, logout


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
        image= request.POST.get('image')

  

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

            patient = Patient.objects.create(user=user,image=image,address=address,city=city,state=state,pincode=pincode)

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
        image= request.POST.get('image')
 

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

            doctor = Doctor.objects.create(user=user,image=image,address=address,city=city,state=state,pincode=pincode)

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
        print(is_doctor)

        try:
            if is_doctor=='doctor':

                user = authenticate(username = login_username,password = login_password)

                if user:
                    login(request, user)
                    messages.info(request,'You are Logged In')
                    return redirect('/profile')
                
                else:
                    messages.warning(request, 'Invalid Credentials')
                    return redirect('/login')

            if is_patient=='patient':

                user = authenticate(username = login_username,password = login_password)

                if user:
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
    if not request.user.is_authenticated :
        messages.warning(request,'Log In needed to see Profile')
        return redirect("home")
    elif request.user.is_authenticated:
        return render(request,template_name='store/profile.html')

    return render(request,template_name='store/profile.html')

    