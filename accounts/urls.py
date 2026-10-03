from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_user, name='login'),

    path('register/', views.register_user, name='register'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('logout/', views.logout_user, name='logout'),

]