from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect



@login_required
def dashboard(request):
    """Vista del panel de control."""
def exit(request):
    logout(request)
    return redirect('dashboard')
