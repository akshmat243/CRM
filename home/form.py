from django import forms
from .models import LeadUser
from .models import ProjectFile

class LeadUserForm(forms.ModelForm):
    class Meta:
        model = LeadUser
        fields = '__all__'


class ExcelUploadForm(forms.Form):
    file = forms.FileField()
    
class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['file']