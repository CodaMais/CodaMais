# Django.
from django.db import models

# Local Django.
from . import constants

# Third-Party.
from redactor.fields import RedactorField


class Theory(models.Model):
    title = models.CharField(max_length=constants.TITLE_FIELD_LENGHT)

    # This is django-wysiwyg-redactor, a text editor application for Django.
    content = RedactorField(verbose_name=u'Text',
                            allow_image_upload=True)

    # Used to send the title of the Theory to admin page.
    def __str__(self):
        return self.title
