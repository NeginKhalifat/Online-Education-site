from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check password match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('accounts:signup')
            else:
                # Check email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already taken')
                    return redirect('accounts:signup')
                else:
                    # Create user
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    return redirect('home')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:signup')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        # Get form values
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'logged out')
        return redirect('index')


