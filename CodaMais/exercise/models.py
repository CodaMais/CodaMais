from django.db import models
from django.core.urlresolvers import reverse
from redactor.fields import RedactorField
from exercise import constants


class Exercise(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    category = models.PositiveIntegerField(choices=constants.CATEGORY_CHOICES)
    statement_question  = RedactorField(verbose_name=u'Text',       #Represents the text and, if any, images referring
                                        allow_file_upload=False,    #to the statement of the exercise.
                                        allow_image_upload=True,
                                        redactor_options={'lang': 'en', 'focus': True},
                                        upload_to='tmp/')
    score = models.PositiveIntegerField()
    deprecated = models.PositiveIntegerField(choices=constants.DEPRECATED_CHOICES)
    input_exercise = models.CharField(max_length=constants.MAX_LENGTH_INPUT)
    output_exercise = models.CharField(max_length=constants.MAX_LENGTH_OUTPUT)

    def __str__(self):
        return self.title
