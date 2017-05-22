# Django.
from django.test import TestCase

# Local Django.
from achievement import constants
from achievement.views import (
    check_if_user_has_achievement
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

    def test_checking_if_user_has_not_achievement(self):
        has_achievement = check_if_user_has_achievement(self.user, self.achievement)
        self.assertFalse(has_achievement)

    def test_checking_if_user_has_achievement(self):
        self.user_achievement.save()
        has_achievement = check_if_user_has_achievement(self.user, self.achievement)
        self.assertTrue(has_achievement)
