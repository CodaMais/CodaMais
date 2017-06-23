# Django.
from django.db import models

# Local Django.
from . import constants

# Third-Party.
from redactor.fields import RedactorField


# Class: Theory
# The class represents the contents that the user can read to learn more about it.
class Theory(models.Model):
    title = models.CharField(verbose_name=u'Title',
                             max_length=constants.TITLE_FIELD_LENGHT)

    # This is django-wysiwyg-redactor, a text editor application for Django.
    content = RedactorField(verbose_name=u'Text',
                            allow_image_upload=True)

    def __str__(self):
        return self.title
