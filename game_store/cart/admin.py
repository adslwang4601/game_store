from django.contrib import admin
from .models import Order


# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['paid', 'order_time']
    list_filter = ['paid', 'order_time']


admin.site.register(Order, OrderAdmin)
