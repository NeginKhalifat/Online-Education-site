from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_page(request):


    return render(request, 'new/index-alt2.html')
