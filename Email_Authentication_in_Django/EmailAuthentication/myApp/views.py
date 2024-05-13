from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, HttpResponse
import random

# Create your views here.

def index(request):
    return render(request, 'index.html')

def generate_otp():
    random_number = random.randint(100000, 999999)
    return random_number

def SignUp(request):
    if request.method == 'GET':
        return redirect('Index')
    
    uname = request.POST['uname']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    try:
        user = User.objects.create_user(username=uname, email=email, password=password)
        user.first_name = fname
        user.last_name = lname
        user.is_active = False
        user.save()
        request.session['uname'] = uname
    except Exception as e:
        return render(request, 'index.html', {'msg': 'Try with different username!'})
    global OTP
    OTP = generate_otp()
    send_mail(
        'OTP to verify your account!',
        f'Your OTP to verify your account is {OTP}\nPlease Do not share OTP with anyone else...',
        'tahabadboy98@gmail.com',
        [email],
        fail_silently=False
    )
    return redirect("validateOTP")

def validateOTP(request):
    if 'uname' in request.session and request.method == 'GET':
        return render(request, 'verifyOTP.html')
    
    elif 'uname' in request.session and request.method == 'POST':
        otp = int(request.POST['otp'])
        if otp == OTP:
            user = User.objects.get(username=request.session['uname'])
            user.is_active = True
            user.save()
            del request.session['uname']
            return HttpResponse("<center><h1>Your account have been registered successfully!</h1><a href='/'>Home</a></center>")
        else:
            return render(request, 'verifyOTP.html', {'msg': 'Incorrect OTP!'})
    return redirect("Index")