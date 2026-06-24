# Helpers for rendering templates, redirecting, and fetching-or-404.
from django.shortcuts import render, redirect, get_object_or_404
# login() logs a user in by creating their session.
from django.contrib.auth import login
# Decorator that forces a function-based view to require login.
from django.contrib.auth.decorators import login_required
# Mixins that add login / custom-permission checks to class-based views.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Django's generic class-based views.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# Q lets us build OR-style database queries (used by the search box).
from django.db.models import Q
# Raised when a database unique constraint is violated (double application).
from django.db import IntegrityError
# Framework for one-time flash messages shown on the next page.
from django.contrib import messages
# Lazily resolves a URL by name (safe to use at class-definition time).
from django.urls import reverse_lazy
# Our models and forms.
from .models import Job, Application, Profile
from .forms import UserRegisterForm, JobForm, ApplicationForm


# --- Role-based access mixins ---------------------------------------------

class RecruiterRequiredMixin(UserPassesTestMixin):
    """Allow the view only if the logged-in user has a Recruiter ('R') profile."""
    def test_func(self):
        # hasattr(...) guards against users (e.g. the superuser) with no Profile.
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'R'


class CandidateRequiredMixin(UserPassesTestMixin):
    """Allow the view only if the logged-in user has a Candidate ('C') profile."""
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'C'


# --- Public & account views ------------------------------------------------

def home(request):
    """Render the landing page."""
    return render(request, 'jobs/home.html')


def register(request):
    """Sign-up view. Creates BOTH a User and a linked Profile (with a role)."""
    # The form was submitted.
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Build the User object but don't save yet — we must hash the password.
            user = form.save(commit=False)
            # set_password() hashes the raw password before storing it.
            user.set_password(form.cleaned_data['password'])
            # Now persist the User row.
            user.save()
            # Create the matching Profile carrying the chosen role + phone.
            Profile.objects.create(
                user=user,
                role=form.cleaned_data.get('role'),
                phone=form.cleaned_data.get('phone')
            )
            # Log the brand-new user straight in for convenience.
            login(request, user)
            # Send them to the home page.
            return redirect('home')
    else:
        # First visit (GET). The desired role can be pre-selected via ?role=R.
        initial_role = request.GET.get('role', 'C')
        form = UserRegisterForm(initial={'role': initial_role})
    # Render the registration page with the (empty or invalid) form.
    return render(request, 'registration/register.html', {'form': form})


# --- Job browsing views ----------------------------------------------------

class JobListView(ListView):
    """Public list of active jobs, with keyword search and job-type filter."""
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        # Start with only ACTIVE jobs, newest first.
        queryset = Job.objects.filter(active=True).order_by('-posted')
        # Read the optional search box (?q=) and job-type dropdown (?jtype=).
        query = self.request.GET.get('q')
        jtype = self.request.GET.get('jtype')

        # Keyword search across title, company and location (OR logic).
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(company__icontains=query) |
                Q(location__icontains=query)
            )
        # Narrow to one employment type if requested.
        if jtype:
            queryset = queryset.filter(jtype=jtype)

        return queryset


class JobDetailView(DetailView):
    """Public detail page for a single job."""
    model = Job
    template_name = 'jobs/job_detail.html'


# --- Candidate actions -----------------------------------------------------

@login_required
def apply_job(request, pk):
    """Let a logged-in candidate apply to a job by uploading a PDF resume."""
    # Find the job or return 404.
    job = get_object_or_404(Job, pk=pk)

    # Recruiters (or anyone whose role isn't Candidate) may not apply.
    if hasattr(request.user, 'profile') and request.user.profile.role != 'C':
        messages.error(request, 'Only candidates can apply for jobs.')
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        # request.FILES carries the uploaded resume file.
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Build the Application but attach job + candidate before saving.
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            try:
                # This may fail if the candidate already applied (unique_together).
                application.save()
                messages.success(request, f'Successfully applied for {job.title} at {job.company}.')
                return redirect('my_applications')
            except IntegrityError:
                # Friendly message instead of a server error on a duplicate apply.
                messages.error(request, 'You have already applied for this job.')
                return redirect('job_detail', pk=pk)
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    """Show the logged-in candidate the list of jobs they have applied to."""
    # Only candidates have applications.
    if hasattr(request.user, 'profile') and request.user.profile.role != 'C':
        messages.error(request, 'Only candidates have applications.')
        return redirect('home')
    # Fetch this candidate's applications, newest first.
    applications = Application.objects.filter(candidate=request.user).order_by('-applied')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


# --- Recruiter actions -----------------------------------------------------

class JobCreateView(LoginRequiredMixin, RecruiterRequiredMixin, CreateView):
    """Recruiters create a new job posting. Requires login + recruiter role."""
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    # Where to go after a successful save.
    success_url = reverse_lazy('recruiter_dashboard')

    def form_valid(self, form):
        # Stamp the current user as the recruiter who owns this job.
        form.instance.recruiter = self.request.user
        messages.success(self.request, 'Job posted successfully.')
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, RecruiterRequiredMixin, UpdateView):
    """Recruiters edit one of THEIR OWN job postings."""
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('recruiter_dashboard')

    def get_queryset(self):
        # Restrict editable jobs to those posted by the logged-in recruiter, so
        # nobody can edit someone else's posting by guessing its id.
        return Job.objects.filter(recruiter=self.request.user)


@login_required
def recruiter_dashboard(request):
    """List the jobs posted by the logged-in recruiter."""
    # Only recruiters may see this dashboard.
    if hasattr(request.user, 'profile') and request.user.profile.role != 'R':
        messages.error(request, 'Only recruiters can access this dashboard.')
        return redirect('home')
    jobs = Job.objects.filter(recruiter=request.user).order_by('-posted')
    return render(request, 'jobs/recruiter_dashboard.html', {'jobs': jobs})


@login_required
def job_applicants(request, pk):
    """Recruiter view of everyone who applied to one of their jobs, plus the
    ability to change an application's status (Applied/Shortlisted/Rejected)."""
    # get_object_or_404 with recruiter=request.user ensures a recruiter can only
    # open the applicants page for their OWN jobs.
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    # All applications for this job, newest first.
    applications = Application.objects.filter(job=job).order_by('-applied')

    # Handle a status-change submission from the applicants table.
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        # Make sure the targeted application really belongs to this job.
        app = get_object_or_404(Application, pk=app_id, job=job)
        # Only accept a status that is one of the valid choices ('A'/'S'/'R').
        if new_status in dict(Application.STATUS).keys():
            app.status = new_status
            app.save()
            messages.success(request, 'Status updated successfully.')
        return redirect('job_applicants', pk=pk)

    return render(request, 'jobs/job_applicants.html', {
        'job': job,
        'applications': applications,
        'status_choices': Application.STATUS,
    })
