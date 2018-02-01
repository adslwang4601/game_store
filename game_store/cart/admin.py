from django.contrib import admin
from .models import Order


# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'paid',
                    'created']
    list_filter = ['paid', 'created']


admin.site.register(Order, OrderAdmin)
