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

    def filtered(self):
        return reverse("leader_board_category",args=[self.slug])

    def search(self):
        return  reverse('search_category',args=[self.slug])

''' Model for game'''
class Game(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(blank=True)
    publisher = models.ForeignKey(User_Profile, on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=False)
    slug = models.SlugField(max_length=200, db_index=True, unique=False)
    # url = models.URLField(unique=True, default="", blank=False)
    url = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    icon = models.URLField(default="http://www.image.com")
    image = models.URLField(default="http://www.image.com")
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('game_detail',
                       args=[self.id, self.slug])

    def game_leaderboard(self):
        return reverse("game_leader_board", kwargs={'game_id': self.id})

    def to_json(self):
        json_list = {
            'id': self.id,
            'name':self.name,
            'category': self.category,
            'description': self.description,
            'price': self.price,
            'publisher':self.publisher.user.username,
            'published_date': self.published_date,
            'image': self.image,
            'icon': self.icon,
            'url': reverse("play_game", kwargs={'game_id': self.id}),
            'scores': reverse("scores", kwargs={'game_id': self.id}),
            'game_leaderboard': reverse("game_leader_board", kwargs={'game_id': self.id})
        }
        return json_list


'''Game sale'''
class Game_Sale(models.Model):
    buyer = models.ForeignKey(User_Profile, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(blank=False,default=timezone.now)
