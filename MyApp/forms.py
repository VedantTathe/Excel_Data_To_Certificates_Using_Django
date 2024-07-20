from django import forms
from .models import ExcelCertifInput

class ExcelCertifInputForm(forms.ModelForm):
    class Meta:
        model = ExcelCertifInput
        fields = ['certificateimg','excelfile', 'column_name']
        widgets = {
            # 'certificateimg': forms.ClearableFileInput(attrs={'autocomplete': 'off'}),
            # 'excelfile': forms.ClearableFileInput(attrs={'autocomplete': 'off'}),
            'column_name': forms.TextInput(attrs={'autocomplete': 'off'}),
        }