# Django's forms framework (ModelForm, fields, widgets).
from django import forms
# The built-in User model, which the registration form is based on.
from django.contrib.auth.models import User
# Our own models that two of the forms are built from.
from .models import Profile, Job, Application


class UserRegisterForm(forms.ModelForm):
    """Sign-up form. It collects the standard User fields PLUS the extra Profile
    fields (role and phone) on a single page. The view splits them apart when
    saving (User in one table, Profile in another)."""
    # Render the password box with dots instead of plain text.
    password = forms.CharField(widget=forms.PasswordInput)
    # Let the new user choose whether they are a Recruiter or Candidate.
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    # Optional phone number stored on the Profile.
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        # These fields map directly onto the built-in User model.
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


class JobForm(forms.ModelForm):
    """Form recruiters use to create or edit a Job posting."""
    class Meta:
        model = Job
        # The recruiter and posted-date are set automatically in the view, so they
        # are deliberately NOT exposed here.
        fields = ['title', 'company', 'location', 'jtype', 'salary', 'description', 'active']


class ApplicationForm(forms.ModelForm):
    """Form candidates use to apply for a job (resume + optional cover note).
    The job and candidate are attached in the view, not chosen by the user."""
    class Meta:
        model = Application
        fields = ['resume', 'cover_note']
