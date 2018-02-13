from django.contrib import admin
from .models import Category, Game

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'publisher', 'category', 'slug', 'url','price', 'published_date']
    list_filter = ['category', 'publisher']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Game, GameAdmin)


