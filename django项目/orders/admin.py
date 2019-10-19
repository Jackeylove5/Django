from django.contrib import admin
from .models import *
# Register your models here.

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name','tel','address','create','update','paid','send']
    list_filter = ['create','update','paid']
    inlines = [OrderItemInline]








