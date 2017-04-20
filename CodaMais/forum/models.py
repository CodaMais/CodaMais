# Django.
from django.db import models

# Third-Party.
from redactor.fields import RedactorField

# local Django.
from forum import constants


class Topic(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    subtilte = models.CharField(max_length=constants.MAX_LENGTH_SUBTITLE)
    autor = models.CharField(max_length=constants.MAX_LENGTH_AUTHOR)
    description = RedactorField(verbose_name=u'Text',
                                allow_file_upload=False,  # Represents the text and, if any image.
                                allow_image_upload=False,    # to the statement of the forum.
                                redactor_options={'lang': 'en', 'focus': True},)
    dateTopic = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title
