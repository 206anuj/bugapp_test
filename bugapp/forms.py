from django import forms
from .models import Bug

class ReportForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['bug_description', 'relevent_section', 'project_owner', 'submitted_by',]