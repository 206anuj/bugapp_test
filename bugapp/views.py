from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from openpyxl.styles import NamedStyle
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font
from .models import Bug
from .forms import ReportForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/bug_list')  # Redirect to 'bug_list' URL name upon successful login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'bugapp/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")  # Optional: Display a logout message
    return redirect('/login')  # Redirect to the login page after logout


@login_required
def report_bug(request):
    if request.method == 'POST':
        bug_description = request.POST.get('bug_description')
        relevent_section = request.POST.get('relevent_section')
        project_owner = request.POST.get('project_owner')
        submitted_by = request.POST.get('submitted_by')  # Assuming you have a form field for this

        # Assign the created_by field to the current logged-in user
        new_bug = Bug.objects.create(
            bug_description=bug_description,
            relevent_section=relevent_section,
            project_owner=project_owner,
            submitted_by=submitted_by,
            # created_by=request.user  # Set the created_by field to the current user
        )

        return redirect('/bug_list')
    else:
        form = ReportForm()
    return render(request, 'bugapp/bug_form.html', {'form': form})


@login_required
def bug_list(request):

    bugs_ordered_by_created_at = Bug.objects.order_by('created_at')

    context = {
        'bugs': bugs_ordered_by_created_at,
    }
    return render(request, 'bugapp/bug_list.html', context=context)


@login_required
def download_bug_list_excel(request):
    # Retrieve Bug objects
    bugs = Bug.objects.all()

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active

    # Set custom number format to display date only (e.g., "yyyy-mm-dd")
    date_style = NamedStyle(name='date_style', number_format='DD-MM-YYYY')  # YYYY-MM-DD

    # Add headers to the Excel file
    ws.append(['IssueDescription', 'ReleventSection (SF)', 'ProjectOwner', 'SubmittedBy', 'CreatedOn', 'CurrentStatus', 'Remarks', 'ClosureDate'])

    # Iterate over each Bug object and add data to Excel
    for bug in bugs:
        # Convert created_at datetime to local timezone
        local_created_at = timezone.localtime(bug.created_at)
        
        # Check if issue_closer_date is None
        if bug.issue_closer_date:
            local_issue_closer_date = timezone.localtime(bug.issue_closer_date).date()
        else:
            local_issue_closer_date = None
        
        # Add row data to Excel worksheet, formatting date using custom style
        ws.append([bug.bug_description, bug.relevent_section, bug.project_owner, bug.submitted_by, local_created_at.date(), bug.automation_team_remark, bug.automation_team_update, local_issue_closer_date])
    
    # Apply custom number format to the "Created At" column (column E, assuming it's the 5th column)
    for cell in ws['E']:
        cell.style = date_style

    # Format the current date and time for the filename
    current_datetime = timezone.now().strftime("%Y%m%d_%H%M%S")
    # Set filename for the Excel file (including date and time)
    filename = f"BugList_{current_datetime}.xlsx"

    # Save the workbook to a response as a file attachment
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Save the workbook content to the HttpResponse
    wb.save(response)

    return response
