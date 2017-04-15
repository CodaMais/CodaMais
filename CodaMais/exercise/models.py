# Django.
from django.db import models
from django.core.urlresolvers import reverse

# Third-Party.
from redactor.fields import RedactorField

# local Django.
from exercise import constants
from user.models import User


class Exercise(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    category = models.PositiveIntegerField(choices=constants.CATEGORY_CHOICES)
    statement_question  = RedactorField(verbose_name=u'Text',
                                        allow_file_upload=False,    # Represents the text and, if any, images referring
                                        allow_image_upload=True,    # to the statement of the exercise.
                                        redactor_options={'lang': 'en', 'focus': True},
                                        upload_to='tmp/')
    score = models.PositiveIntegerField()
    deprecated = models.PositiveIntegerField(choices=constants.DEPRECATED_CHOICES)

    def __str__(self):
        return self.title


class UserExercise(models.Model):
    class Meta:
        unique_together = (('user', 'exercise'),)

    number_submission = models.PositiveIntegerField(default = 1)
    code = models.TextField()
    status = models.BooleanField(default = False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
    )
    # the unit of measurement of time is seconds
    time = models.CharField(max_length=constants.MAX_LENGTH_TIME)

    def update_or_creates(self, source_code, exercise, user, time, status):
        if self:
            # Update the current exercise of the user.
            self.number_submission += 1
        else:
            # Create the current exercise for the user.
            self = UserExercise()

        self.user = user
        self.exercise = exercise
        self.status = status
        self.time = time
        self.code = source_code
        self.save()

    def __str__(self):
        return self.user.email + "-" + str(self.exercise.id)


class TestCase(models.Model):
    input_exercise = models.TextField(max_length=constants.MAX_LENGTH_INPUT)
    output_exercise = models.TextField(max_length=constants.MAX_LENGTH_OUTPUT)
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="test_cases",
    )

    def __str__(self):
        return self.input_exercise + "-" + self.output_exercise
