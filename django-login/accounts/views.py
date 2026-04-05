from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm
import random

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def password_reset_request(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            code = str(random.randint(100000, 999999))
            request.session['reset_code'] = code
            request.session['reset_email'] = email
            send_mail(
                'Your password reset code',
                f'Your reset code is: {code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return redirect('password_reset_verify')
        except User.DoesNotExist:
            error = 'No account found with this email.'
    return render(request, 'accounts/password_reset.html', {'error': error})

def password_reset_verify(request):
    error = None
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == request.session.get('reset_code'):
            return redirect('password_reset_confirm')
        else:
            error = 'Invalid code. Please try again.'
    return render(request, 'accounts/password_reset_verify.html', {'error': error})

def password_reset_confirm(request):
    error = None
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error = 'Passwords do not match.'
        else:
            email = request.session.get('reset_email')
            try:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                del request.session['reset_code']
                del request.session['reset_email']
                return redirect('login')
            except User.DoesNotExist:
                error = 'Something went wrong. Please start over.'
    return render(request, 'accounts/password_reset_confirm.html', {'error': error})