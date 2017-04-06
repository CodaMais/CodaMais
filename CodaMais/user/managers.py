# standard library
import logging

# Django
from django.contrib.auth.models import BaseUserManager

# logger instance
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, email, password, username, first_name, **kwargs):
        logger.info("Creating user.")

        user = self.model(email=self.normalize_email(email),
                          username=username,
                          first_name=first_name,
                          is_active=False,
                          **kwargs)

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password,
                         first_name, **kwargs):
        logger.info("Creating superuser.")

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          is_staff=True,
                          is_active=True,
                          is_superuser=True,
                          **kwargs)

        user.set_password(password)
        user.save(using=self.db)

        return user
