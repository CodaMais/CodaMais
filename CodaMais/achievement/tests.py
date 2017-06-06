# Django.
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage

# Local Django.unlock_achievementunlock_achievement
from achievement import constants
from achievement.views import (
    check_if_user_has_achievement, unlock_achievement, check_achievement_user_should_get
)
from achievement.models import (
    Achievement, UserAchievement
)
from user.models import User


class TestAchievementRegistration(TestCase):
    achievement = Achievement()

    def setUp(self):
        self.achievement.name = 'Senhor do C'
        self.achievement.description = 'Realizou com sucesso 100 códigos em C.'
        self.achievement.achievement_type = constants.CORRECT_EXERCISE_ACHIEVEMENTS
        self.achievement.quantity = 100

    def test_str_is_correct(self):
        self.achievement.save()
        achievement_data = Achievement.objects.get(name=self.achievement.name)
        self.assertEqual(str(achievement_data), str(self.achievement))


class TestUserAchievementRegistration(TestCase):
    user = User()
    achievement = Achievement()
    user_achievement = UserAchievement()

    def setUp(self):
        # Creating a achievement in database.
        self.achievement.name = 'Senhor do C'
        self.achievement.description = 'Realizou com sucesso 100 códigos em C.'
        self.achievement.achievement_type = constants.CORRECT_EXERCISE_ACHIEVEMENTS
        self.achievement.quantity = 100
        self.achievement.save()

        # Creating a user in database.
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.score = 10
        self.user.is_active = True
        self.user.save()

        # Creating the relationship between User and Achievement in database.
        self.user_achievement.user = self.user
        self.user_achievement.achievement = self.achievement
        self.user_achievement.save()

    def test_str_is_correct(self):
        user_achievement_data = UserAchievement.objects.get(user=self.user, achievement=self.achievement)
        self.assertEqual(str(user_achievement_data), str(self.user_achievement))

    def test_update_or_creates_is_correct(self):
        # Creating a new achievement in database.
        new_achievement = Achievement()
        new_achievement.name = 'New Achievement'
        new_achievement.description = 'New Achievement Description.'
        new_achievement.achievement_type = constants.CORRECT_EXERCISE_ACHIEVEMENTS
        new_achievement.quantity = 100
        new_achievement.save()

        # Creating a new relationship between User and Achievement in database.
        new_user_achievement = UserAchievement()
        new_user_achievement.update_or_creates(self.user, new_achievement)

        new_user_achievement_data = UserAchievement.objects.get(user=self.user, achievement=new_achievement)
        self.assertEqual(str(new_user_achievement_data), str(new_user_achievement))


class TestAchievementView(TestCase):
    user = User()
    achievement = Achievement()
    user_achievement = UserAchievement()

    def setUp(self):
        # Creating a achievement in database.
        self.achievement.name = 'Senhor do C'
        self.achievement.description = 'Chegou a 10 de Score.'
        self.achievement.achievement_type = constants.SCORE_ACHIEVEMENTS
        self.achievement.quantity = 10
        self.achievement.save()

        # Creating a user in database.
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.score = 10
        self.user.is_active = True
        self.user.save()

        # Creating the relationship between User and Achievement in database.
        self.user_achievement.user = self.user
        self.user_achievement.achievement = self.achievement

        self.factory = RequestFactory()

    def test_checking_if_user_has_not_achievement(self):
        has_achievement = check_if_user_has_achievement(self.user, self.achievement)
        self.assertFalse(has_achievement)

    def test_checking_if_user_has_achievement(self):
        self.user_achievement.save()
        has_achievement = check_if_user_has_achievement(self.user, self.achievement)
        self.assertTrue(has_achievement)

    def test_unlocking_achievement(self):
        unlock_achievement(self.user, self.achievement)

        user_achievement_data = UserAchievement.objects.get(user=self.user, achievement=self.achievement)
        self.assertEqual(str(user_achievement_data), str(self.user_achievement))

    def test_checking_if_user_should_get_the_achievement(self):
        # List of achievements that have the same type(SCORE ACHIEVEMENTS).
        achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.SCORE_ACHIEVEMENTS)

        # The list of achievements must be ordered by the biggest quantity of correct exercises.
        achievements_list = achievements_list.order_by('-quantity')

        request = self.factory.get('/achievement/')

        # This is necessary to test with messages.
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        check_achievement_user_should_get(self.user, self.user.score, achievements_list, request)

        user_achievement_data = UserAchievement.objects.get(user=self.user, achievement=self.achievement)
        self.assertEqual(str(user_achievement_data), str(self.user_achievement))

    def test_checking_if_user_should_not_get_the_achievement(self):
        # The user had already unlocked this achievement.
        self.user_achievement.save()

        # List of achievements that have the same type(SCORE ACHIEVEMENTS).
        achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.SCORE_ACHIEVEMENTS)

        # The list of achievements must be ordered by the biggest quantity of correct exercises.
        achievements_list = achievements_list.order_by('-quantity')

        request = self.factory.get('/achievement/')

        user_achievement_data = UserAchievement.objects.get(user=self.user, achievement=self.achievement)

        check_achievement_user_should_get(self.user, self.user.score, achievements_list, request)

        self.assertEqual(str(user_achievement_data), str(self.user_achievement))

    def test_checking_if_user_should_not_get_any_achievement(self):
        # User should have a score under than the smaller achievement quantity attribute.
        self.user.score = 0

        # List of achievements that have the same type(SCORE ACHIEVEMENTS).
        achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.SCORE_ACHIEVEMENTS)

        # The list of achievements must be ordered by the biggest quantity of correct exercises.
        achievements_list = achievements_list.order_by('-quantity')

        request = self.factory.get('/achievement/')

        check_achievement_user_should_get(self.user, self.user.score, achievements_list, request)

        self.assertRaises(UserAchievement.DoesNotExist,
                          UserAchievement.objects.get,
                          user=self.user, achievement=self.achievement)
