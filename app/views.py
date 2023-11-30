from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from app.models import *
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dotenv import load_dotenv
import random
import os
import requests
from datetime import datetime as dt
import datetime
import re
load_dotenv()
# Create your views here.
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')        
        weatherAPI="c7a0c39b6f052d08a865b6391550658d"
        # weatherAPI=os.getenv('weatherAPI')
        print(weatherAPI)
        
        if request.method=="POST":
            city=request.POST['city']
            complete_api_link="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+weatherAPI
            api_link=requests.get(complete_api_link)
            api_data=api_link.json()
            if api_data['cod']=="404":
                d={'username':username,'MSG':'ENTER VALID CITY NAME'}
                return render(request,'app/home.html',d)
            else:
                tempreture=((api_data['main']['temp'])-273.15)
                description=api_data['weather'][0]['description']
                humidity=api_data['main']['humidity']
                wind_speed=api_data['wind']['speed']
                icon=api_data['weather'][0]['icon']
                time=dt.now().strftime("%H:%M:%S")
                day=datetime.date.today().strftime("%A")
                date=dt.now().strftime("%Y-%m-%d")

                UO = User.objects.filter(username=username)
                UserHistory = History.objects.create(user=UO[0],city=city,date=date,time=time)
                UserHistory.save()


                d={'username':username,'city':city.capitalize(),'tempreture':f"{tempreture:.2f}",'description':description.title(),'humidity':humidity,'wind_speed':wind_speed,'icon':icon,'time':time,'day':day}
                return render(request,'app/home.html',d)
        else:
            city="bangalore"
            complete_api_link="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+weatherAPI
            api_link=requests.get(complete_api_link)
            api_data=api_link.json()

            tempreture=((api_data['main']['temp'])-273.15)
            description=api_data['weather'][0]['description']
            humidity=api_data['main']['humidity']
            wind_speed=api_data['wind']['speed']
            icon=api_data['weather'][0]['icon']
            time=dt.now().strftime("%H:%M:%S")
            day=datetime.date.today().strftime("%A")

            d={'username':username,'city':city.capitalize(),'tempreture':f"{tempreture:.2f}",'description':description.title(),'humidity':humidity,'wind_speed':wind_speed,'icon':icon,'time':time,'day':day}
            return render(request,'app/home.html',d)
    return render(request,'app/home.html')

def register(request):
    if request.session.get('username'):
        logout(request)
    if request.method=="POST":
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        pword=request.POST['password']
        usersearchlist=User.objects.filter(username=username)
        if len(usersearchlist)==0:
            UO=User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=pword)
            UO.save()
            send_mail('Registration',
                      'you have successfully completed your registration process for login use your registered email and password ',
                      "subirbehera1999@gmail.com",
                      [UO.email],
                      fail_silently=False)
            MSG="Registration Successful"
            d={'MSG':MSG}
            return render(request,'app/register.html',d)
        else:
            MSG="Username Already Exists"
            d={'MSG':MSG}
            return render(request,'app/register.html',d)
    return render(request,'app/register.html')

def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('app:home'))
        else:
            MSG="Invalid User or Password"
            d={'MSG':MSG.upper()}
            return render(request,'app/login.html',d)
    return render(request,'app/login.html')
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:home'))

def forgetpassword(request):
    if request.method=="POST":
        username=request.POST["username"]
        QSU=User.objects.filter(username=username)
        if len(QSU)!=0:
            UO=QSU[0]
            global vmail
            vmail = UO.email
            global CODE
            CODE=random.randint(1000,9999)
            send_mail('Reset password',
                      f"Hi {UO.first_name},\nSorry to hear you're having trouble logging into weather  forecasting app. We got a message that you foregot your password. If it was you, you can get right back to your account by reset your password. Your OTP is {CODE}",
                      'subirbehera1999@gmail.com',
                      [UO.email],
                      fail_silently=False)
            return HttpResponseRedirect(reverse('app:vcode'))
        else:
            MSG="ENTER REGISTERED E-MAIL"
            d={'MSG':MSG}
            return render(request,'app/forgetpassword.html',d)
    return render(request,'app/forgetpassword.html')
def vcode(request):
    d={'vmail':vmail}
    if request.method=="POST":
        code=request.POST['vcode']
        if CODE==int(code):
            return HttpResponseRedirect(reverse('app:reset_password'))
    return render(request,'app/vcode.html',d)

def reset_password(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST["password"]
        rpassword=request.POST["rpassword"]
        QSU=User.objects.filter(email=email)
        if len(QSU)!=0:
            if password==rpassword:
                UO=QSU[0]
                UO.set_password(request.POST['password'])
                UO.save()
                return HttpResponseRedirect(reverse('app:login'))
            else:
                MSG="password doesn't match"
                d={'MSG':MSG.upper()}
                return render(request,'app/reset_password.html',d)
        else:
            MSG='Enter valid E-mail address'
            d={'MSG':MSG.upper()}
            return render(request,'app/reset_password.html',d)
    return render(request,'app/reset_password.html')

def history(request):
    history=History.objects.all()
    d={'history':history}
    if request.method=="POST":
        cityortime=request.POST['cityortime']
        if re.match('\d{0,2}:\d{0,2}:\d{0,2}',cityortime):
            History.objects.filter(time=cityortime).delete()
        else:
            History.objects.filter(city=cityortime).delete()
        histories=History.objects.all()
        d1={'histories':histories}
        return render(request,'app/history.html',d1)    
    return render(request,'app/history.html',d)
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        msg=request.POST['msg']
        send_mail(f'Message By {name} from weatherAPI',
                      f"Name: {name}\nE-mail: {email}\n\n{msg}",
                      email,
                      ["subirbehera1999@gmail.com"],
                      fail_silently=False)
        MSG="Message sent successfully..."
        d={'MSG':MSG}
        return render(request,'app/contact.html',d)
    return render(request,'app/contact.html')
