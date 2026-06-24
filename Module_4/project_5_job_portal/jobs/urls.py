# path() builds individual URL rules.
from django.urls import path
# Django's ready-made login/logout views, so we don't have to write them.
from django.contrib.auth import views as auth_views
# This app's own views.
from . import views

# Note: this app does NOT set app_name, so its URLs are referenced by plain
# names like 'job_list' (not 'jobs:job_list').
urlpatterns = [
    # --- Public / account pages ---
    # Landing page.
    path('', views.home, name='home'),
    # Custom registration view (creates a User + a Profile with a role).
    path('register/', views.register, name='register'),
    # Built-in login view, told to use our custom template.
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Built-in logout view.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- Browsing & applying to jobs (candidate side) ---
    # List of all active jobs, with search + job-type filtering.
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    # Detail page for a single job.
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    # Apply to a job (upload resume). Login + candidate role required.
    path('job/<int:pk>/apply/', views.apply_job, name='apply_job'),
    # A candidate's own list of submitted applications.
    path('my-applications/', views.my_applications, name='my_applications'),

    # --- Managing jobs (recruiter side) ---
    # A recruiter's dashboard listing the jobs they posted.
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    # Post a brand-new job.
    path('job/new/', views.JobCreateView.as_view(), name='job_create'),
    # Edit one of your own job postings.
    path('job/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    # View and update the status of everyone who applied to one of your jobs.
    path('job/<int:pk>/applicants/', views.job_applicants, name='job_applicants'),
]
