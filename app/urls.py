from django.urls import path
from app.views import *
app_name='app'

urlpatterns = [
    path('home/',home,name="home"),
    path('register/',register,name="register"),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('forgetpassword/',forgetpassword,name="forgetpassword"),
    path('vcode/',vcode,name="vcode"),
    path('reset_password/',reset_password,name="reset_password"),
    path('history/',history,name="history"),
    path('contact/',contact,name="contact"),
    
]