from django.db import models

# Create your models here.
class AdminModel(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.name}'
    

class FileModel(models.Model):
    admin = models.ForeignKey(AdminModel, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.admin.name} - {self.file.name}'
    
