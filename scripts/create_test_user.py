#!/usr/bin/env python
"""
Create or ensure demo executive user exists for local development and testing.
"""
import os
import sys
import django

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

DEMO_USER = os.getenv('DEMO_USERNAME', 'executive')
DEMO_PASS = os.getenv('DEMO_PASSWORD', 'RetailMart2026!')
DEMO_EMAIL = os.getenv('DEMO_EMAIL', 'executive@retailmart.com')

def ensure_user():
    if not User.objects.filter(username=DEMO_USER).exists():
        User.objects.create_superuser(
            username=DEMO_USER,
            email=DEMO_EMAIL,
            password=DEMO_PASS
        )
        print(f"Created demo superuser: '{DEMO_USER}'")
    else:
        u = User.objects.get(username=DEMO_USER)
        u.set_password(DEMO_PASS)
        u.is_superuser = True
        u.is_staff = True
        u.save()
        print(f"Updated demo user password: '{DEMO_USER}'")

if __name__ == '__main__':
    ensure_user()
