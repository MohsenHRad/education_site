from django.contrib import admin

from account_module.models import UserModel


# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username','date_joined', 'is_active']


admin.site.register(UserModel, UserModelAdmin)
