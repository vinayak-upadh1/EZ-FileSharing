from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home_view, name='home'),
    path("ops/home", views.admin_home_view),
    path("ops/login", views.login_view),
    path("ops/signup", views.signup_view),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("ops/<str:email>", views.verification_view),
    path("ops/<str:email>/dashboard", views.dashboard_view, name='dashboard'),  
    path("ops/<str:email>/upload", views.upload_file_view, name='upload_file'), 

]