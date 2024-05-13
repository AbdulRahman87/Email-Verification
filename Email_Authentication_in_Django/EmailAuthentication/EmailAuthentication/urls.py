from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="Index"),
    path('signup/', views.SignUp, name="signup"),
    path('validateotp/', views.validateOTP, name="validateOTP")
]
