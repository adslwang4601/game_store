from django.test import TestCase

# Create your tests here.
# Create your tests here.
from django.test import TestCase
from .models import User_Profile
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class ModelsTest(TestCase):

    """
    Luigi
    Testing creation and update of Profile objects.
    """
    def testProfile(self):
        self.us1 = User.objects.create(username="player1", password="12345678", email="player1@gmail.com")
        user1 = User_Profile.objects.create(user=self.us1)
        players_group = Group.objects.create(name='players')
        players_group.user_set.add(user1.user)

        # Test creation
        # Create user
        self.assertEqual(user1.user.username, 'player1')
        self.assertEqual(user1.user.password, '12345678')
        self.assertEqual(user1.user.email, 'player1@gmail.com')

        # Create Group
        self.assertIn(players_group.name, [group.name for group in Group.objects.all()])
        self.assertIn('players', [group.name for group in user1.user.groups.all()])

        # Test Modification
        # Modify user
        user1.user.username = "player2"
        self.assertEqual(user1.user.username, "player2")
        user1.user.password = "87654321"
        self.assertEqual(user1.user.password, "87654321")
        user1.user.email = "none@gmail.com"
        self.assertEqual(user1.user.email, "none@gmail.com")

        #