# Register your models here.
from django.contrib import admin
from api.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("partial_total",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]

admin.site.register(Order, OrderAdmin)