from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import CustomUserCreationForm 
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from ops.models import FileModel
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse
from django.core.mail import send_mail



def client_home(request):
    return render(request, "client/client_home.html", {})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # verification_link = f"http://127.0.0.1:8000/ops/{email}"
            # send_mail("Verify your email", f"Click on this link to verify your email: {verification_link}", "vinayakport8080@gmail.com", [email])
        
            login(request, user) 
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'client/client_signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password1', None)

        user = CustomUser.objects.filter(email=email).first()

        if user is not None and check_password(password, user.password):
            login(request, user)
            messages.success(request, 'User login successful')
            dashboard_url = reverse("client:dashboard_view", kwargs={'email': user.email})
            return redirect(dashboard_url)
        else:
            messages.error(request, 'Either you have not verified your account or your login credentials are wrong!!')

    form = CustomUserCreationForm()  
    return render(request, 'client/client_login.html', {'form': form})

@login_required(login_url='client:login')
def dashboard_view(request, email):
    files = FileModel.objects.all()
    context = {
        'files': files,
    }
    return render(request, 'client/client_dashboard.html', context)

@login_required(login_url='client:login')
def download_view(request, file_id):
    file_object = get_object_or_404(FileModel, id=file_id)

    file_path = os.path.join(settings.MEDIA_ROOT, file_object.file.name)

    if os.path.exists(file_path):
        try:
            return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        except FileNotFoundError:
            raise Http404("File not found.")
    else:
        raise Http404("File not found.")
   