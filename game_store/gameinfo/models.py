from django.db import models
from Profile.models import User_Profile
from django.contrib.auth.models import User
from django.utils import timezone
'''Model for categories'''
class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return str(self.name)

''' Model for game'''
class Game(models.Model):
    '''
    Image sizes
    - icon:  48x48
    - image: 256x256
    '''
    title = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField()
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=False)
    url = models.URLField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    icon = models.ImageField("Game icon", null=True, blank=True, upload_to="games/icons")
    image = models.ImageField("Game image", null=True, blank=True, upload_to="games/image")
    published_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)

'''Game score'''
class Game_Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    score = models.PositiveIntegerField(blank=False)
    date = models.DateTimeField(blank=False, default=timezone.now)

'''Game sale'''
class Game_Sale(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(blank=False,default=timezone.now)
# Create your models here.
