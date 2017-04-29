from django.contrib import admin
from forum.models import (
    Topic, Answer
)


class ForumAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'date_topic']


class ForumAnswerAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'topic',
                    'description']


admin.site.register(Topic, ForumAdmin)
admin.site.register(Answer, ForumAnswerAdmin)
