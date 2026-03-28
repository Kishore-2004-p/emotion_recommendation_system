from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home_view(request):
    """Landing page / home view"""
    if request.user.is_authenticated:
        # Redirect authenticated users based on role
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_panel:dashboard')
        else:
            return redirect('user_dashboard:dashboard')
    else:
        # Show landing page for anonymous users
        return redirect('accounts:login')
