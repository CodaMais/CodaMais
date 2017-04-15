from django.contrib import admin
from exercise.models import *


# admin.site.register(Exercise)
admin.site.register(UserExercise)
# admin.site.register(TestCase)


class TestCasesInLine(admin.TabularInline):
    model = TestCase
    extra = 0

@admin.register(Exercise)
class ProfileExercise(admin.ModelAdmin):

    list_display = ("title", "category", "statement_question", "score", "deprecated", "show_test_cases")

    search_fields = ["title"]

    inlines = [
        TestCasesInLine
    ]

    def show_test_cases(self, obj):
        return obj.test_cases.all().count()
