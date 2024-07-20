from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class ExcelCertifInput(models.Model):
    certificateimg = models.ImageField(upload_to='certificates/')
    excelfile = models.FileField(upload_to='excelfiles/')
    column_name = models.CharField(max_length=200)
    
    def __str__(self):
        return f'Certificates Input {self.id}'
    
    