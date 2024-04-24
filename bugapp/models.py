from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bug(models.Model):

    bug_description = models.CharField(max_length=1024)
    relevent_section = models.CharField(max_length=64)
    project_owner = models.CharField(max_length=64)
    submitted_by = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    automation_team_update = models.CharField(max_length=32, null=True, blank=True, default='')
    automation_team_remark = models.CharField(max_length=1024, null=True, blank=True, default='')
    issue_closer_date = models.DateTimeField(blank=True, null=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bugs_created', blank=True, null=True) 

    def __str__(self):
        return f"{self.bug_description} || {self.relevent_section} || {self.project_owner} || {self.submitted_by} || {self.created_at}"