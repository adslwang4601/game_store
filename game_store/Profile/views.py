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
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required



# log_in view
def user_login(request):
    # If user has been authenticated,
    if request.user.is_authenticated:
        return render(request, 'game/dashboard.html')

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # returns a User object if the credentials are valid for a backend
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'game/dashboard.html')
                else:
                    return HttpResponse('Disabled account')
    else:
        form = LoginForm()
    return render(request, 'Profile/log_in.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.is_active = False
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            # Create the user profile
            user_profile = User_Profile.objects.create(user=new_user)
            user_profile.save()

            # If User apply as developer, create developers group and permission
            if user_form.cleaned_data['applyAsDeveloper']:
                devs_group, created = Group.objects.get_or_create(name='developers')
                devs_group.user_set.add(user_profile.user)
                content_type = ContentType.objects.get_for_model(User_Profile)
                permission_developer, created = Permission.objects.get_or_create(
                    codename='developers',
                    name='Developers',
                    content_type=content_type
                )
                user_profile.user.user_permissions.add(permission_developer)

            # If User apply as player, create players group and permission
            else:
                players_group, created = Group.objects.get_or_create(name='players')
                players_group.user_set.add(user_profile.user)
                content_type = ContentType.objects.get_for_model(User_Profile)
                permission_players, created = Permission.objects.get_or_create(
                    codename='players',
                    name='Players',
                    content_type=content_type
                )
                user_profile.user.user_permissions.add(permission_players)


            # activationrue
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'

            message = render_to_string('Profile/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            # email will be showed in the console
            email.send()
            # activation page
            return render(request, 'Profile/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                'token': account_activation_token.make_token(new_user),
            })
            # redirect()
    else:
        user_form = RegistrationForm()
    return render(request, 'Profile/register.html', {'form': user_form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # if user is not None and account_activation_token.check_token(user, token):
    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'Profile/register_done.html', {'new_user': user})
    else:
        return HttpResponse('Activation link is invalid!')

@login_required(login_url='log_in')
def edit(request):
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

@login_required(login_url='log_in')
def my_profile(request):
    user_form = UserEditForm(instance=request.user,
                             data=request.POST)
    profile_form = ProfileEditForm(instance=request.user.user_profile,
                                   data=request.POST,
                                   files=request.FILES)
    return render(request, 'Profile/user_profile.html', {'user_form': user_form,
                                                         'profile_form': profile_form})
