from .models import User_Profile
from django.contrib.auth.models import Group, User, Permission


def save_profile(backend, user, response, *args, **kwargs):
    print ('!!!!!!!!!!!')
    if backend.name == 'facebook':
        print ('!!!!!!!!!!!')
        if not User_Profile.objects.filter(user=user).exists():
            user_profile = User_Profile.objects.create(user=user)
            user_profile.save()
            players_group = Group.objects.get(name='players')
            players_group.user_set.add(user_profile.user)
            permission_players = Permission.objects.get(codename='players')
            user_profile.user.user_permissions.add(permission_players)

    return {}
