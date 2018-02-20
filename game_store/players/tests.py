from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from players.models import Game_Score, Saved_Game
from gameinfo.models import Game, Category
from Profile.models import User_Profile
from django.contrib.auth.models import User,Group
class ModelsTest(TestCase):

    def testGame_Score(self):

        user = User.objects.create(username='user', password='test12345678', email='ss@gmail.com')
        profile = User_Profile.objects.create(user=user)
        group = Group.objects.create(name='players')
        user.groups.add(group)
        category = Category.objects.create(name='action', slug='action')
        game = Game.objects.create(name='SuperMario', description='None', publisher=profile, category=category,
                                    slug='mario', url='http://www.baidu.com', price=20,
                                    icon='https://www.myimage.com', image='https://www.myimage.com')
        profile._ownedGames.add(game)

        game_score = Game_Score.objects.create(played_game=game, score=10, _player=profile)

        # Test creation
        self.assertEqual(game_score.played_game, game)
        self.assertEqual(game_score.score, 10)
        self.assertEqual(game_score._player,profile)

    def testSaved_Game(self):
        user = User.objects.create(username='user', password='test12345678', email='ss@gmail.com')
        profile = User_Profile.objects.create(user=user)
        group = Group.objects.create(name='players')
        user.groups.add(group)
        category = Category.objects.create(name='action', slug='action')
        game = Game.objects.create(name='SuperMario', description='None', publisher=profile, category=category,
                                   slug='mario', url='http://www.baidu.com', price=20,
                                   icon='https://www.myimage.com', image='https://www.myimage.com')
        profile._ownedGames.add(game)

        saved_game = Saved_Game.objects.create(played_game=game, state = "LOAD",_player=profile)

        self.assertEqual(saved_game.played_game,game)
        self.assertEqual(saved_game.state,"LOAD")
        self.assertEqual(saved_game._player,profile)

        # Test modification
        # modify status
        saved_game.state = "SAVE"
        self.assertEqual(saved_game.state,"SAVE")
# Create your tests here.
