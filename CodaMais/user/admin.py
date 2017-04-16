from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username',
                    'first_name',
                    'email',
                    'is_active',
                    'password',
                    'user_image']


admin.site.register(User, UserAdmin)
