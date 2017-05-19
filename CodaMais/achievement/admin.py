# Django
from django.contrib import admin

# local Django
from achievement.models import (
    Achievement, UserAchievement
)


class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'description',
                    'achievement_type',
                    'quantity']


class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'achievement']


admin.site.register(Achievement, AchievementAdmin)
admin.site.register(UserAchievement, UserAchievementAdmin)
