from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from .models import User_Profile


def user_login(request):
    if request.user.is_authenticated():
        messages.warning(request, "You are already logged in.")
        return HttpResponseRedirect(redirect_to=reverse('profile'))
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # returns a User object if the credentials are valid for a backend
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # render(request, reverse('home_page'))
                    return HttpResponseRedirect(redirect_to=reverse('home_page'))
    else:
        form = LoginForm()
        return render(request, reverse('log_in'), {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = User_Profile.objects.create(user=new_user)
            profile.save()
            return render(request,
                          reverse('register_done'),
                          {'new_user': new_user})
    else:
        user_form = RegistrationForm()
        return render(request, reverse('register'),{'user_form': user_form})

