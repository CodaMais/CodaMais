'''
    Copyright (C) 2017, CodaMais.
    License: GNU General Public License v3.0, see LICENSE.txt
    App: exercise
    File: models.py
    Contains all classes related to the exercise, it is django's default to keep all models in single file.
'''

# Python
import logging

# Django
from django.db import models
from django.db.models import Sum
from django.utils.timezone import datetime, now
from django.db.models.functions import TruncMonth

# third-party
from redactor.fields import RedactorField

# local Django
from exercise import constants
from user.models import User
from theory.models import Theory

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(constants.PROJECT_NAME)


# Class: Exercise
# The class represents the exercises register by admin.
class Exercise(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)

    category = models.PositiveIntegerField(choices=constants.CATEGORY_CHOICES)

    # Represents the text and, if any, images referring
    # to the statement of the exercise.
    statement_question = RedactorField(
                        verbose_name=u'Text',
                        allow_file_upload=False,
                        allow_image_upload=True,
                        redactor_options={'lang': 'en', 'focus': True},
                        upload_to='tmp/')

    score = models.PositiveIntegerField()

    deprecated = models.PositiveIntegerField(
                choices=constants.DEPRECATED_CHOICES)

    tip = models.CharField(max_length=constants.MAX_LENGTH_TIP)

    theory = models.ForeignKey(
        Theory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,)

    def new_exercises():
        exercises = Exercise.objects.all().order_by('-id')[:5]
        return exercises

    def __str__(self):
        return self.title


class UserExercise(models.Model):
    class Meta:
        unique_together = (('user', 'exercise'),)

    number_submission = models.PositiveIntegerField(default=0)

    code = models.TextField(blank=False, null=False, default=constants.DEFAULT_CODE)

    status = models.BooleanField(default=False)

    user = models.ForeignKey(
          User,
          on_delete=models.CASCADE,)

    exercise = models.ForeignKey(
            Exercise,
            on_delete=models.CASCADE,)

    # The unit of measurement of time is seconds.
    time = models.CharField(max_length=constants.MAX_LENGTH_TIME,
                            default=0)

    scored = models.BooleanField(default=False)

    date_submission = models.DateTimeField(auto_now_add=True, blank=True)

    def update_or_creates(self, source_code, exercise, user, time, status, scored):
        self.number_submission += 1
        self.user = user
        self.exercise = exercise
        self.status = status
        self.time = time
        self.code = source_code
        self.scored = scored
        self.date_submission = now()
        self.save()
        return self

    def __str__(self):
        return self.user.email + "-" + str(self.exercise.id)


class UserExerciseSubmission(models.Model):
    user_exercise = models.ForeignKey(
          UserExercise,
          on_delete=models.CASCADE,)
    scored = models.BooleanField(default=False)
    submissions = models.IntegerField(default=1)
    date_submission = models.DateTimeField(auto_now_add=True, blank=True)

    def submissions_by_day(user, days_ago_date):
        # Get the number of submissions by day for all user exercises.
        submissions_by_day = UserExerciseSubmission.objects.filter(
            user_exercise__user=user,
            date_submission__gte=days_ago_date
        ).annotate(month=TruncMonth('date_submission')).values('month').annotate(
            submissions=Sum('submissions')
        ).annotate(
            corrects=Sum('scored')
        ).values('date_submission', 'corrects', 'submissions')
        return submissions_by_day

    def updates_submission(user_exercise_submission, user_exercise):

        # The number of submissions will be increment only if is not true that
        # the current submission has scored (true) and exercise is correct (true).
        if not (user_exercise_submission.scored is True and user_exercise.status is True):
            user_exercise_submission.submissions += 1
        else:
            pass

        # Updates today's exercise submission "scored" to the exercise status.
        user_exercise_submission.scored = user_exercise.status
        user_exercise_submission.save()

    def submit(user_exercise):
        # Finds a existing one submission or creates a new one.
        today = datetime.today()

        submission, created = UserExerciseSubmission.objects.get_or_create(
            user_exercise=user_exercise,
            date_submission__year=today.year,
            date_submission__month=today.month,
            date_submission__day=today.day,
            defaults={"scored": user_exercise.status}
        )

        # If a new user excercise submission is not created
        if created is False:
            # then updates the found user excercise submission.
            UserExerciseSubmission.updates_submission(submission, user_exercise)
        else:
            # Nothing to do.
            pass

        return submission

    def __str__(self):
        return self.user_exercise.exercise.title + "-" + str(self.user_exercise.id)


class TestCaseExercise(models.Model):
    input_exercise = models.TextField(max_length=constants.MAX_LENGTH_INPUT)

    output_exercise = models.TextField(max_length=constants.MAX_LENGTH_OUTPUT)

    exercise = models.ForeignKey(
              Exercise,
              on_delete=models.CASCADE,
              related_name="test_cases",)

    def __str__(self):
        return self.input_exercise + "-" + self.output_exercise
