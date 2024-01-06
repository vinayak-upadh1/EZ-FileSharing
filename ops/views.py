from django.shortcuts import render, redirect, HttpResponse
from .models import AdminModel, FileModel
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_view(request):
    return render(request, 'home.html', {})

def admin_home_view(request):
    return render(request, 'admin/admin_home.html', {})

def signup_view(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        verification_link = f"http://127.0.0.1:8000/ops/{email}"
        send_mail("Verify your email", f"Click on this link to verify your email: {verification_link}", "vinayakport8080@gmail.com", [email])
        
        object = AdminModel(name=name, email=email, password=password)
        object.save()
        return render(request, 'admin/admin_home.html', {})
    return render(request, "admin/admin_signup.html", {})

def login_view(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            admin = AdminModel.objects.get(email=email, password=password)
            messages.success(request, 'Admin login successful')
            # return render(request, 'admin_dashboard.html', {}) 
            return redirect('dashboard', email=email)

        except AdminModel.DoesNotExist:
            messages.error(request, 'Either you have not verified your account or your login credentials are wrong!!')
    return render(request, 'admin/admin_login.html', {})  

def verification_view(request, email):
    object = AdminModel.objects.get(email=email)
    object.is_verified=True 
    object.save()
    context = {
        'data' : 'Your account has been verified successfully!!. Please continue to login'
    }
    return render(request, 'admin/admin_login.html', context)

def dashboard_view(request, email):
    try:
        admin = AdminModel.objects.get(email=email)
        files = FileModel.objects.filter(admin=admin)
        return render(request, 'admin/admin_dashboard.html', {'admin': admin, 'files': files})
    except AdminModel.DoesNotExist:
        return render(request, 'admin/admin_signup.html', {'message': 'Admin not found'})
    
def upload_file_view(request, email):
    if request.method == 'POST' and 'file' in request.FILES:
        admin = AdminModel.objects.get(email=email)
        file_model = FileModel(admin=admin, file=request.FILES['file'])
        file_model.save()
        # You may want to add success/failure messages here
        messages.success(request, 'File uploaded successfully')
        
        return redirect('dashboard', email=email)
    return render(request, 'admin/upload_file.html') 
        


