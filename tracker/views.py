from django.shortcuts import render,redirect,get_object_or_404
from .forms import JobForm, RegisterForm
from .models import Job
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
import csv
from datetime import date,timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

#s collections import Counter
# Create your views here.
def home_view(request):
    return render(request, 'tracker/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')  # or wherever you want
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    query = request.GET.get('query', '')
    status = request.GET.get('status', '')

    jobs = Job.objects.filter(user=user)

    if query:
        jobs = jobs.filter(company__icontains=query)

    if status:
        jobs = jobs.filter(status=status)

    today = date.today()
    soon = today + timedelta(days=3)
    upcoming = jobs.filter(deadline__range=[today, soon])

    stats = {
        'Applied': jobs.filter(status='Applied').count(),
        'Interview': jobs.filter(status='Interview').count(),
        'Offer': jobs.filter(status='Offer').count(),
        'Rejected': jobs.filter(status='Rejected').count(),
        'Shortlisted': jobs.filter(status='Shortlisted').count(),
        'Assessment': jobs.filter(status='Assessment').count(),
        'Hired': jobs.filter(status='Hired').count(),
        
    }

    return render(request, 'tracker/dashboard.html', {
        'jobs': jobs,
        'upcoming': upcoming,
        'stats': stats,
    })

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user  # 🛑 If your model has a user field
            job.save()
            messages.success(request, "✅ Job added successfully!")
            return redirect('dashboard')  # or your desired page
        else:
            print("❌ Form errors:", form.errors)
            messages.error(request, "Form is invalid. Please fix the errors.")
    else:
        form = JobForm()
    return render(request, 'tracker/add_job.html', {'form': form})




@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            # 🔍 Last Resort Debug Prints
            job = form.save(commit=False)
            print("📋 Debug Info Before Save:")
            print("Company:", job.company)
            print("Position:", job.position)
            print("Link:", job.link)
            print("Date Applied:", job.date_applied)
            print("Deadline:", job.deadline)
            print("Status:", job.status)
            print("User:", job.user)

            job.user = request.user
            job.save()

            print("✅ Job Saved Successfully.")
            return redirect('dashboard')
        else:
            print("❌ Form Errors:", form.errors)
    else:
        form = JobForm(instance=job)

    return render(request, 'tracker/edit_job.html', {'form': form})


@login_required
def delete_job(request, job_id):
    job = Job.objects.get(id=job_id, user=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('dashboard')
    return render(request, 'tracker/delete_job.html', {'job': job})

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_applications.csv"'

    writer = csv.writer(response)
    writer.writerow(['Company', 'Position', 'Status', 'Deadline'])

    jobs = Job.objects.filter(user=request.user)
    for job in jobs:
        writer.writerow([job.company, job.position, job.status, job.deadline])

    return response

def job_list(request):
    jobs = Job.objects.all().order_by('-date_applied')  # or 'deadline'
    return render(request, 'tracker/job_list.html', {'jobs': jobs})


def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)

    if request.method == 'POST':
        job.delete()
        return redirect('dashboard')

    return render(request, 'tracker/delete_job.html', {'job': job})