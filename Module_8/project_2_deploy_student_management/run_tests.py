# Standard library import for accessing operating-system features (here: env vars).
import os
# Import sys so we can reconfigure the console output stream below.
import sys
# Import Django so we can boot its framework machinery from a plain script.
import django

# Windows terminals default to the legacy "cp1252" encoding, which cannot print
# Unicode symbols such as the "✓" check mark used in the messages below. We force
# the standard output stream to UTF-8 so the script runs identically on every OS.
try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, ValueError):
    # Older Python versions (or redirected streams) may not support reconfigure();
    # in that rare case we simply continue with the default encoding.
    pass

# Tell Django which settings module to use before we call django.setup().
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
# Initialise Django (loads apps, models and settings) so we can use the ORM/Client.
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from students.models import Student

def test_everything():
    client = Client()
    
    print("Testing Visitor Access...")
    # Test index page
    response = client.get('/')
    assert response.status_code == 200, f"Index failed with {response.status_code}"
    print("✓ Index page loaded successfully (Visitor)")
    
    # Test login page
    response = client.get('/accounts/login/')
    assert response.status_code == 200, f"Login page failed with {response.status_code}"
    print("✓ Login page loaded successfully")

    # Test register page
    response = client.get('/accounts/register/')
    assert response.status_code == 200, f"Register page failed with {response.status_code}"
    print("✓ Register page loaded successfully")

    # Test detail page of a student
    student = Student.objects.first()
    if student:
        response = client.get(f'/{student.pk}/')
        assert response.status_code == 200, f"Detail page failed with {response.status_code}"
        print("✓ Student detail page loaded successfully")
        
        # Test protected views (should redirect to login for visitors)
        response = client.get(f'/{student.pk}/edit/')
        assert response.status_code in [301, 302], f"Edit page didn't redirect visitor, got {response.status_code}"
        print("✓ Edit page properly protected from visitors")
        
        response = client.get(f'/{student.pk}/delete/')
        assert response.status_code in [301, 302], f"Delete page didn't redirect visitor, got {response.status_code}"
        print("✓ Delete page properly protected from visitors")
        
    print("\nTesting Authenticated Staff Access...")
    # Log in as the seeded superuser
    login_success = client.login(username='admin', password='admin')
    assert login_success, "Failed to login with admin credentials"
    print("✓ Logged in as Staff/Admin successfully")
    
    # Now try accessing protected views
    response = client.get('/add/')
    assert response.status_code == 200, f"Add student page failed with {response.status_code}"
    print("✓ Add student page loaded successfully for staff")
    
    if student:
        response = client.get(f'/{student.pk}/edit/')
        assert response.status_code == 200, f"Edit student page failed with {response.status_code}"
        print("✓ Edit student page loaded successfully for staff")
        
        response = client.get(f'/{student.pk}/delete/')
        assert response.status_code == 200, f"Delete student confirmation page loaded successfully for staff"
        print("✓ Delete student page loaded successfully for staff")
    
    print("\nAll endpoints tested successfully. No errors or crashes found!")

if __name__ == '__main__':
    test_everything()
