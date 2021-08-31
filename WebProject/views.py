from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_page(request):
    Admin = False
    if request.user.username == 'negin':
        Admin = True

    return render(request, 'home.html', {'admin': Admin})
