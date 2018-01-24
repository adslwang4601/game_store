from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm, UserEditForm, ProfileEditForm
from .models import User_Profile
from django.contrib.auth.views import login
from django.contrib.auth.models import Group, User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text

def user_login(request):
    if request.user.is_authenticated:
        # messages.warning(request, "You are already logged in.")
        return HttpResponseRedirect(redirect_to=reverse_lazy('dashboard'))
    # else:
    #     return login(request, template_name='Profile/log_in.html')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # returns a User object if the credentials are valid for a backend
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to=reverse_lazy('dashboard'))
    else:
        form = LoginForm()
    return render(request, 'Profile/log_in.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.is_active= False
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            # Create the user profile
            user_profile = User_Profile.objects.create(user=new_user)
            user_profile.save()

            # activation
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            if  user_form.cleaned_data['applyAsDeveloper ']:
                devs = Group.objects.get(name='developers')
                devs.user_set.add(user_profile.user)

            else:
                players =  Group.objects.get(name='players')
                players.user_set.add(user_profile.user)

            return render(request,
                          'Profile/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = RegistrationForm()
    return render(request, 'Profile/register.html', {'form': user_form})


def edit(request):
    # profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.user_profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        # profile = Profile.objects.get(user=request.user)
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.user_profile)
    return render(request, 'Profile/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


def my_profile(request):
    user_form = UserEditForm(instance=request.user,
                             data=request.POST)
    profile_form = ProfileEditForm(instance=request.user.user_profile,
                                   data=request.POST,
                                   files=request.FILES)
    return render(request, 'Profile/user_profile.html', {'user_form': user_form,
                                                        'profile_form': profile_form})