from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description','publisher', 'category','slug','price'
    'published_date']
    list_filter = ['category', 'publisher']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

# Register your models here.
