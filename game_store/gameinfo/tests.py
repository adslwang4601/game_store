import sys
sys.path.append('..')
from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Category, Game
from Profile.models import User_Profile
# Create your tests here.

class ModelsTest(TestCase):

    def testGame(self):
        user1 = User.objects.create(username='user1', password='test12345678', email='ss@gmail.com')
        profile1 = User_Profile.objects.create(user=user1)
        group1 = Group.objects.create(name='players')
        user1.groups.add(group1)

        category1 = Category.objects.create(name='action', slug='action')
        category2 = Category.objects.create(name='puzzle', slug='puzzle')

        game1 = Game.objects.create(name='SuperMario', description='None', publisher=profile1, category=category1,
                                    slug='mario', url='http://www.baidu.com', price=20,
                                    icon='https://www.myimage.com', image='https://www.myimage.com')
        game2 = Game.objects.create(name='Snake', description='None', publisher=profile1, category=category2,
                                    slug='snake', url='http://www.qq.com', price=20,
                                    icon='https://www.myimage.com', image='https://www.myimage.com')
        profile1._ownedGames.add(game1)
        profile1._ownedGames.add(game2)

        # test model creation
        self.assertEqual(profile1._ownedGames.get(pk=game1.pk), game1)
        self.assertEqual(profile1._ownedGames.get(pk=game2.pk), game2)
        self.assertEqual(game1.name, 'SuperMario')
        self.assertEqual(game1.description, 'None')
        self.assertEqual(game1.publisher, profile1)
        self.assertEqual(game1.category, category1)
        self.assertEqual(game1.slug, 'mario')
        self.assertEqual(game1.url, 'http://www.baidu.com')
        self.assertEqual(game1.price, 20)
        self.assertEqual(game1.image, 'https://www.myimage.com')
        self.assertEqual(game1.icon, 'https://www.myimage.com')

        # test model modification
        game1.name = 'SuperMario1'
        self.assertEqual(game1.name, 'SuperMario1')
        game1.description = 'something'
        self.assertEqual(game1.description, 'something')


    def testCategory(self):

        user1 = User.objects.create(username='user1', password='test12345678', email='ss@gmail.com')
        profile1 = User_Profile.objects.create(user=user1)
        category1 = Category.objects.create(name='action', slug='action')
        game1 = Game.objects.create(name='SuperMario', description='None', publisher=profile1, category=category1,
                                    slug='mario', url='http://www.baidu.com', price=20,
                                    icon='https://www.myimage.com', image='https://www.myimage.com')

        # test model creation
        self.assertEqual(category1.name, 'action')

        # test model modification
        category1.name = 'FPS'
        self.assertEqual(category1.name, 'FPS')









