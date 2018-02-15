from django.db import models
# from django.contrib.auth.models import User
from Profile.models import User_Profile
from django.utils import timezone
from django.urls import reverse
'''Model for categories'''
class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('game_list_by_category',
                       args=[self.slug])

''' Model for game'''
class Game(models.Model):
    '''
    Image sizes
    - icon:  48x48
    - image: 256x256
    '''
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField()
    publisher = models.ForeignKey(User_Profile, on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=False)
    slug = models.SlugField(max_length=200, db_index=True, unique=False)
    url = models.URLField(unique=True, default="", blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    icon = models.URLField(default="http://www.yourimage.com")
    image = models.URLField(default="http://www.yourimage.com")
    # icon = models.ImageField("Game icon", null=True, blank=True, upload_to="games/icons")
    # image = models.ImageField("Game image", null=True, blank=True, upload_to="games/image")

    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('game_detail',
                       args=[self.id, self.slug])

    def to_json(self, player=None):
        json_list = {
            'id': self.id,
            'name':self.name,
            'category': self.category,
            'description': self.description,
            'price': self.price,
            'publisher':self.publisher.user.username,
            'published_date': str(self.published_date),
            'image': self.image,
            'icon': self.icon,
            'url': reverse("play_game", kwargs={'game_id': self.id}),
            # 'leaderboard_url': reverse("leader_board_game", kwargs={'game_id': self.id})
        }

        if player is not None and isinstance(player, User_Profile) and player.is_authenticated:
            whether_owned = player.user_profile._ownedGames.filter(id=self.id)
            if whether_owned.count()>0:
                json_list['owned'] = True
            else:
                json_list['owned'] = False

        return json_list

'''Game score'''
class Game_Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    player = models.ForeignKey(User_Profile, on_delete=models.CASCADE, blank=False)
    score = models.PositiveIntegerField(blank=False)
    date = models.DateTimeField(blank=False, default=timezone.now)

'''Game sale'''
class Game_Sale(models.Model):
    buyer = models.ForeignKey(User_Profile, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(blank=False,default=timezone.now)
# Create your models here.
