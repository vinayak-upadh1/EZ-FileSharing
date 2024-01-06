# from django.contrib import admin
# from django.urls import path
# from . import views

# urlpatterns = [
#     path("client/home", views.signup_view),
#     path("client/login", views.login_view),
#     path("client/signup", views.signup_view),
#     path("client/<str:email>", views.verification_view),
#     path("client/<str:email>/dashboard", views.dashboard_view, name='dashboard'),  
# ]

# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, login_view, client_home, dashboard_view, download_view

app_name = 'client'

urlpatterns = [
    path('home/', client_home),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/<str:email>/', dashboard_view, name='dashboard_view'),
    path('download/<int:file_id>/', download_view, name='download_view'), 

    # Add other urlpatterns as needed
]
