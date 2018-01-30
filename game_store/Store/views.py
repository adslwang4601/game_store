# -*- coding: utf-8 -*-
from django.shortcuts import render

def dashboard(request):
    # backend = request.session['_auth_user_backend']
    return render(request, 'game/dashboard.html')
# Create your views here.
