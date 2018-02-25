from .models import User_Profile
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType


def save_profile(backend, user, response, *args, **kwargs):
    print ('!!!!!!!!!!!')
    if backend.name == 'facebook':
        print ('!!!!!!!!!!!')
        if not User_Profile.objects.filter(user=user).exists():
            user_profile = User_Profile.objects.create(user=user)
            user_profile.save()
            content_type = ContentType.objects.get_for_model(User_Profile)
            players_group, created = Group.objects.get_or_create(name='players')
            players_group.user_set.add(user_profile.user)
            permission_players, created = Permission.objects.get_or_create( codename='players',
                    name='Players',
                    content_type=content_type)
            user_profile.user.user_permissions.add(permission_players)

    return {}
