from django.contrib import admin

from . import models


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['price', 'subject', 'name']
    list_display = ['name', 'owner', 'subject', 'price', 'created_date', 'is_active']
    list_editable = ['price', 'is_active']


class CategoryAdmin(admin.ModelAdmin):
    # list_filter = ['name', 'parent', 'is_active']
    list_display = ['name', 'url_title', 'is_active', 'parent']
    list_editable = ['is_active', 'parent']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory, CategoryAdmin)
admin.site.register(models.ProductComment)
