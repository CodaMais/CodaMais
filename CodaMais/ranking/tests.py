# Django
from django.test import TestCase
from django.test.client import RequestFactory

# local Django
from user.models import (
    User,
)
from .views import (
    show_ranking,
    get_users_with_bigger_score
)

# RESPONSE CODES.
REQUEST_SUCCEEDED = 200  # 200 is return with success response.

# 302 is the value returned from a HttpRequest status code when the URL was redirected.
REQUEST_REDIRECT = 302


class RankingViewTest(TestCase):
    user = User()
    userTwo = User()
    userThree = User()
    userFour = User()
    userFive = User()
    userSix = User()

    def setUp(self):
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.user.set_password('userpassword')
        self.user.save()

        self.userTwo.email = "user2@user.com"
        self.userTwo.first_name = "TestUser"
        self.userTwo.username = "Username2"
        self.userTwo.is_active = True
        self.userTwo.set_password('userpassword')
        self.userTwo.save()

        self.userThree.email = "user3@user.com"
        self.userThree.first_name = "TestUser"
        self.userThree.username = "Username3"
        self.userThree.is_active = True
        self.userThree.set_password('userpassword')
        self.userThree.save()

        self.userFour.email = "user4@user.com"
        self.userFour.first_name = "TestUser"
        self.userFour.username = "Username4"
        self.userFour.is_active = True
        self.userFour.set_password('userpassword')
        self.userFour.save()

        self.userFive.email = "user5@user.com"
        self.userFive.first_name = "TestUser"
        self.userFive.username = "Username5"
        self.userFive.is_active = True
        self.userFive.set_password('userpassword')
        self.userFive.save()

        self.userSix.email = "user6@user.com"
        self.userSix.first_name = "TestUser"
        self.userSix.username = "Username6"
        self.userSix.is_active = True
        self.userSix.set_password('userpassword')
        self.userSix.save()

        self.factory = RequestFactory()

    def test_show_ranking(self):
        request = self.factory.get('/ranking/ranking/')
        request.user = self.user
        response = show_ranking(request)
        self.assertEqual(response.status_code, REQUEST_SUCCEEDED)

    def test_get_users_with_big_score(self):
        userList = get_users_with_bigger_score()

        self.assertIsNotNone(userList)
