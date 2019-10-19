from django.contrib import admin
from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # prepopulated_fields用于让slug字段通过name字段自动生成
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id",'name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']    # 列表过滤器
    list_editable = ['price', 'available']   # 在后台管理直接修改
    prepopulated_fields = {'slug': ('name',)}