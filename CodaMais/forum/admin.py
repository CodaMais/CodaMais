from django.contrib import admin
from forum.models import Topic


class ForumAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'dateTopic']


admin.site.register(Topic, ForumAdmin)
