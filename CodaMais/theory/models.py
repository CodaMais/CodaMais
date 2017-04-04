from django.db import models
from redactor.fields import RedactorField
from . import constants


class Theory(models.Model):
    title = models.CharField(max_length=constants.TITLE_FIELD_LENGHT)
    content = RedactorField(verbose_name=u'Text')

    # Used to send the title of the Theory to admin page
    def __str__(self):
        return self.title
