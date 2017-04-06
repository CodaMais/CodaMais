# standard library
import datetime

# Django
from django.test import TestCase

# local Django
from .models import User
from .models import UserProfile
from .forms import UserRegisterForm


class UserTest(TestCase):
    email = "user@user.com"
    password = "userpassword"
    first_name = "User"
    username = "Username"

    def setUp(self):
        User.objects.create_user(email=self.email,
                                 password=self.password,
                                 first_name=self.first_name,
                                 username=self.username)

    def test_user_get_short_name(self):
        user = User.objects.get(email=self.email)
        self.assertEqual(self.email, user.get_short_name())

    def test_user_get_full_name(self):
        user = User.objects.get(email=self.email)
        self.assertEqual(self.email, user.get_full_name())


class UserProfileTest(TestCase):
    email = "user@user.com"
    password = "userpassword"
    first_name = "User"
    username = "Username"
    user = User()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    activation_key = "5c262e9f57ce25652eaefb4ca697191f395f39eb"
    new_profile = UserProfile()

    def setUp(self):
        self.user = User.objects.create_user(email=self.email,
                                             password=self.password,
                                             first_name=self.first_name,
                                             username=self.username)

        self.new_profile = UserProfile(user=self.user,
                                       activation_key=self.activation_key,
                                       key_expires=self.key_expires)

    def test_if_profile_is_not_null(self):
        self.assertIsNotNone(self.new_profile)

    def test_str(self):
        self.assertEqual(self.new_profile.__str__(), self.username)


class MetaTest(TestCase):
    def test_verbose_name(self):
        verbose_name = u'Perfil de Usuario'
        self.assertEquals(verbose_name, u'Perfil de Usuario')


class UserRegisterFormTest(TestCase):
    email = "user@user.com"
    password = "userpassword"
    first_name = "User"
    username = "Username"
    valid_form = {}
    invalid_form = {}

    def setUp(self):
        self.valid_form = {'email': self.email,
                           'password': self.password,
                           'first_name': self.first_name,
                           'username': self.username,
                           'password_confirmation': self.password}

        self.invalid_form = {'email': '',
                             'password': self.password,
                             'first_name': self.first_name,
                             'username': self.username,
                             'password_confirmation': self.password}

    def test_UserRegisterForm_valid(self):
        user_form = UserRegisterForm(self.valid_form)
        self.assertTrue(user_form.is_valid())

    def test_UserRegisterForm_email_invalid(self):
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_username_exists_in_database(self):
        User.objects.create_user(email=self.email,
                                 password=self.password,
                                 first_name=self.first_name,
                                 username=self.username)

        user_form = UserRegisterForm(self.valid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_username_invalid(self):
        self.invalid_form['username'] = 'Us'
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_first_name_invalid(self):
        self.invalid_form['first_name'] = 'User1'
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_email_exists_in_database(self):
        User.objects.create_user(email=self.email,
                                 password=self.password,
                                 first_name=self.first_name,
                                 username='TestUser')

        user_form = UserRegisterForm(self.valid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_password_invalid(self):
        self.invalid_form['password'] = 'aaa'
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_confirm_password_invalid(self):
        self.invalid_form['password_confirmation'] = 'userpasswordd'
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())
