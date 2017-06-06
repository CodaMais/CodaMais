# standard library
import datetime

# Django
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage

# local Django
from user.views import (
    register_view, login_view,
)
from .models import (
    User, UserProfile, RecoverPasswordProfile,
)
from exercise.models import (
    Exercise, UserExercise
)
from .forms import (
    UserRegisterForm, UserEditForm, ConfirmPasswordForm, RecoverPasswordForm, UserLoginForm,
)
from django.test import Client


class ProfileViewTest(TestCase):
    email = "user@user.com"
    password = "userpassword"
    first_name = "Username"
    username = "Username"
    factory = RequestFactory()

    def setUp(self):
        self.user = User.objects.create_user(email=self.email,
                                             password=self.password,
                                             first_name=self.first_name,
                                             username=self.username)

    def test_if_profile_page_is_showing(self):
        c = Client()
        response = c.get("/pt-br/user/profile/Username/")
        self.assertEqual(response.status_code, 200)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.user = User()
        self.email = "user@user.com"
        self.wrong_email = "useruser.com"
        self.password = "userpassword"
        self.first_name = "TestUser"
        self.username = "Username"
        self.form = (
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'password_confirmation': self.password,
                'email': self.email,
            }
        )
        self.wrong_form = self.form
        self.factory = RequestFactory()

    # This will happen when user is already logged.
    def test_if_register_page_is_not_showing(self):
        self.user.save()
        request = self.factory.get('/user/register', follow=True)
        request.user = self.user
        response = register_view(request)
        self.assertEqual(response.status_code, 302)

    def test_if_register_was_made(self):
        request = self.factory.post('user/register/', self.form, follow=True)

        # This is necessary to test with messages.
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        request.user = User()
        request.user.id = None
        response = register_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_if_register_was_invalid(self):
        self.wrong_form['email'] = self.wrong_email
        request = self.factory.post('user/register/', self.form, follow=True)
        request.user = User()
        request.user.id = None
        response = register_view(request)

        # If register was invalid, we reload the same page.
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User()
        self.user.email = "user@user.com"
        self.user.email = "useruser.com"
        self.user.password = "userpassword"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.factory = RequestFactory()
        self.user.save()

    # This will happen when user is already logged.
    def test_if_login_page_is_not_showing(self):
        request = self.factory.get('/user/login/')
        request.user = self.user
        response = login_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/dashboard')


class UserTest(TestCase):

    def setUp(self):
            self.user = User()
            self.user.email = "user@user.com"
            self.user.password = "userpassword"
            self.user.first_name = "TestUser"
            self.user.username = "Username"
            self.user.score = 100

            self.first_user = User()
            self.first_user.email = "second_user@user.com"
            self.first_user.password = "userpassword"
            self.first_user.first_name = "TestUser"
            self.first_user.username = "Second_Username"
            self.first_user.score = 200

    def test_user_get_short_name(self):
        User.objects.create_user(email=self.user.email,
                                 password=self.user.password,
                                 first_name=self.user.first_name,
                                 username=self.user.username)

        user = User.objects.get(email=self.user.email)
        self.assertEqual(self.user.email, user.get_short_name())

    def test_user_get_full_name(self):
        User.objects.create_user(email=self.user.email,
                                 password=self.user.password,
                                 first_name=self.user.first_name,
                                 username=self.user.username)
        user = User.objects.get(email=self.user.email)
        self.assertEqual(self.user.email, user.get_full_name())

    def test_get_current_ranking_position(self):
        self.user.save()
        position = self.user.get_position()
        self.assertEqual(1, position)

    def test_if_current_ranking_position_is_second(self):
        self.first_user.save()
        self.user.save()
        self.assertEqual(2, self.user.get_position())

    def test_if_current_ranking_position_is_first(self):
        second_user = self.first_user
        second_user.score = 50
        second_user.save()
        self.user.save()
        self.assertEqual(1, self.user.get_position())

    def test_if_current_user_dont_do_correct_exercise(self):
        self.user.save()
        self.assertEqual(0, self.user.get_correct_exercises())

    def test_if_current_user_has_one_exercise(self):
        self.exercise = Exercise()
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.exercise.save()
        self.user_exercise = UserExercise()
        self.user_exercise.scored = False
        self.user_exercise.code = """
                                    #include <stdio.h>
                                    int main () {
                                                char c;
                                                scanf("%c", &c);
                                                printf("B");
                                                return 0;
                                                }
                                                """
        self.user.id = 1
        self.user_exercise.user = self.user
        self.user_exercise.exercise = self.exercise
        self.user_exercise.status = True
        self.user.save()
        self.user_exercise.save()
        self.assertEqual(100, self.user.get_correct_exercises())


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
    password = "userpassword"
    first_name = "User"
    username = "Username"
    valid_form = {}
    invalid_form = {}

    def setUp(self):
        self.user = User.objects.create_user(email=self.email,
                                             password=self.password,
                                             first_name=self.first_name,
                                             username=self.username)

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


class UserEditFormTest(TestCase):
    email = "user@user.com"
    wrong_email = "useruser.com"
    password = "userpassword"
    wrong_password = "userpassw"
    wrong_password_max = 'userpasswordd'
    wrong_password_min = 'pas'
    first_name = "TestUser"
    wrong_first_name = "#123#sas,"
    username = "Username"
    valid_form = {}

    def setUp(self):
        User.objects.create_user(email=self.email,
                                 password=self.password,
                                 first_name=self.first_name,
                                 username=self.username)

        self.valid_form = {'first_name': self.first_name,
                           'password': self.password,
                           'password_confirmation': self.password}

    def test_UserEditForm_valid(self):
        form = UserEditForm(self.valid_form)
        self.assertTrue(form.is_valid())

    def test_UserEditForm_password_min_size_invalid(self):
        self.valid_form['password'] = self.wrong_password_min
        form = UserEditForm(self.valid_form)
        self.assertFalse(form.is_valid())

    def test_UserEditForm_password_max_size_invalid(self):
        self.valid_form['password'] = self.wrong_password_max
        form = UserEditForm(self.valid_form)
        self.assertFalse(form.is_valid())

    def test_UserEditForm_password_confirmation_invalid(self):
        self.valid_form['password'] = 'codaMenos'
        form = UserEditForm(self.valid_form)
        self.assertFalse(form.is_valid())

    def test_UserEditForm_valid_null_password(self):
        self.valid_form['password'] = ''
        form = UserEditForm(self.valid_form)
        self.assertTrue(form.is_valid())
