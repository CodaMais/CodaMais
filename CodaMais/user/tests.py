# standard library
import datetime

# Django
from django.test import TestCase
from django.test.client import RequestFactory

# local Django
from .models import User
from .models import UserProfile
from .models import RecoverPasswordProfile
from .forms import ConfirmPasswordForm
from .forms import RecoverPasswordForm
from .forms import UserRegisterForm
from .forms import UserLoginForm
from user.views import register_view


class RegisterViewTest(TestCase):
    user = User()
    email = "user@user.com"
    wrong_email = "useruser.com"
    password = "userpassword"
    first_name = "TestUser"
    username = "Username"
    factory = RequestFactory()

    def test_if_register_page_is_showing(self):
        request = self.factory.get('/register')
        response = register_view(request)
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):
    factory = RequestFactory()

    def test_if_login_page_is_showing(self):
        request = self.factory.get('/login')
        response = register_view(request)
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    factory = RequestFactory()

    def test_if_logout_page_is_showing(self):
        request = self.factory.get('/register')
        response = register_view(request)
        self.assertEqual(response.status_code, 200)


class UserTest(TestCase):
    email = "user@user.com"
    wrong_email = "useruser.com"
    password = "userpassword"
    first_name = "TestUser"
    username = "Username"

    def test_user_get_short_name(self):
        User.objects.create_user(email=self.email,
                                 password=self.password,
                                 first_name=self.first_name,
                                 username=self.username)

        user = User.objects.get(email=self.email)
        self.assertEqual(self.email, user.get_short_name())

    def test_user_get_full_name(self):
        User.objects.create_user(email=self.email,
                                 password=self.password,
                                 first_name=self.first_name,
                                 username=self.username)
        user = User.objects.get(email=self.email)
        self.assertEqual(self.email, user.get_full_name())


class UserAdminTest(TestCase):
        email = "user@user.com"
        password = "userpassword"
        first_name = "User"

        def setUp(self):
            User.objects.create_superuser(email=self.email,
                                          password=self.password,
                                          first_name=self.first_name)

        def test_admin_user_get_short_name(self):
            user = User.objects.get(email=self.email)
            self.assertEqual(self.email, user.get_short_name())


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
    first_name = "Username"
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

    def test_UserRegisterForm_username_min_size_invalid(self):
        self.invalid_form['username'] = 'Us'
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_username_max_size_invalid(self):
        self.invalid_form['username'] = '1234567890111'
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

    def test_UserRegisterForm_password_min_size_invalid(self):
        self.invalid_form['password'] = 'pas'
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_password_max_size_invalid(self):
        self.invalid_form['password'] = 'passwordInvalid'
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())

    def test_UserRegisterForm_confirm_password_invalid(self):
        self.invalid_form['password_confirmation'] = 'userpasswordd'
        user_form = UserRegisterForm(self.invalid_form)
        self.assertFalse(user_form.is_valid())


class RecoverPasswordProfileTest(TestCase):
    email = "user@user.com"
    password = "userpassword"
    first_name = "User"
    username = "Username"
    user = User()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    activation_key = "5c262e9f57ce25652eaefb4ca697191f395f39eb"
    new_profile = RecoverPasswordProfile()

    def setUp(self):
        self.user = User.objects.create_user(email=self.email,
                                             password=self.password,
                                             first_name=self.first_name,
                                             username=self.username)

        self.new_profile = RecoverPasswordProfile(user=self.user,
                                                  activation_key=self.activation_key,
                                                  key_expires=self.key_expires)

    def test_if_profile_is_not_null(self):
        self.assertIsNotNone(self.new_profile)

    def test_str(self):
        self.assertEqual(self.new_profile.__str__(), self.username)


class RecoverPasswordFormTest(TestCase):
    email = "user@user.com"
    valid_form = {}
    invalid_form = {}

    def setUp(self):
        self.valid_form = {'email': self.email}

        self.invalid_form = {'email': ''}

    def test_UserRegisterForm_valid(self):
        recover_password_form = RecoverPasswordForm(self.valid_form)
        self.assertTrue(recover_password_form.is_valid())

    def test_UserRegisterForm_email_invalid(self):
        recover_password_form = RecoverPasswordForm(self.invalid_form)
        self.assertFalse(recover_password_form.is_valid())


class ConfirmPasswordFormTest(TestCase):
    password = "userpassword"
    password_confirmation = "userpassword"
    valid_form = {}
    invalid_form = {}

    def setUp(self):
        self.valid_form = {'password': self.password,
                           'password_confirmation': self.password_confirmation}

        self.invalid_form = {'password': self.password,
                             'password_confirmation': self.password_confirmation}

    def test_ConfirmPasswordForm_password_min_size_invalid(self):
        self.invalid_form['password'] = 'pas'
        confirm_password_form = ConfirmPasswordForm(self.invalid_form)
        self.assertFalse(confirm_password_form.is_valid())

    def test_ConfirmPasswordForm_password_max_size_invalid(self):
        self.invalid_form['password'] = 'passwordInvalid'
        confirm_password_form = ConfirmPasswordForm(self.invalid_form)
        self.assertFalse(confirm_password_form.is_valid())

    def test_ConfirmPasswordForm_confirm_password_invalid(self):
        self.invalid_form['password_confirmation'] = 'userpasswo'
        confirm_password_form = ConfirmPasswordForm(self.invalid_form)
        self.assertFalse(confirm_password_form.is_valid())

    def test_ConfirmPasswordForm_confirm_password_valid(self):
        self.invalid_form['password_confirmation'] = 'userpassword'
        confirm_password_form = ConfirmPasswordForm(self.invalid_form)
        self.assertTrue(confirm_password_form.is_valid())


class UserLoginFormTest(TestCase):
    password = "userpassword"
    password_confirmation = "userpassword"
    valid_form = {}
    invalid_form = {}

    def setUp(self):
        self.valid_form = {'password': self.password,
                           'password_confirmation': self.password_confirmation}

        self.invalid_form = {'password': self.password,
                             'password_confirmation': self.password_confirmation}

    def test_UserLoginForm_password_min_size_invalid(self):
        self.invalid_form['password'] = 'pas'
        user_login_form = UserLoginForm(self.invalid_form)
        self.assertFalse(user_login_form.is_valid())

    def test_UserLoginForm_password_max_size_invalid(self):
        self.invalid_form['password'] = 'passwordInvalid'
        user_login_form = UserLoginForm(self.invalid_form)
        self.assertFalse(user_login_form.is_valid())

    def test_UserLoginForm_confirm_password_invalid(self):
        self.invalid_form['password_confirmation'] = 'userpasswordd'
        user_login_form = UserLoginForm(self.invalid_form)
        self.assertFalse(user_login_form.is_valid())
