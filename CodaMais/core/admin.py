from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'password', 'is_active']


admin.site.register(User, UserAdmin)
