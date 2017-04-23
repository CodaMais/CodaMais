# Django
from django.contrib import admin

# local Django
from exercise.models import (
    Exercise, UserExercise, TestCaseExercise
)


admin.site.register(UserExercise)


class TestCasesInLine(admin.TabularInline):
    model = TestCaseExercise
    extra = 0


@admin.register(Exercise)
class ProfileExercise(admin.ModelAdmin):

    list_display = ("title", "category", "statement_question", "score",
                    "deprecated", "show_test_cases")

    search_fields = ["title"]

    inlines = [
        TestCasesInLine
    ]

    def show_test_cases(self, obj):
        return obj.test_cases.all().count()
