from django import forms
from .models import ExcelCertifInput

class ExcelCertifInputForm(forms.ModelForm):
    class Meta:
        model = ExcelCertifInput
        fields = ['certificateimg','excelfile', 'column_name']