# standard library
import logging

# Local Django
from achievement import constants
from exercise.models import UserExercise
from forum.models import Answer
from achievement.models import (
    Achievement, UserAchievement
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Find all achievements related to corrected exercises and determine if the current user
# is able to unlock some of them.
def verify_correct_exercise_achievement(user):
    logger.info("Verifying correct exercise achievement!")
    user_corrected_exercise_quantity = get_user_corrected_exercise_quantity(user)

    # List of achievements that have the same type(correct exercise).
    correct_exercise_achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.CORRECT_EXERCISE_ACHIEVEMENTS)

    # The list of achievements must be ordered by the biggest quantity of correct exercises.
    correct_exercise_achievements_list = correct_exercise_achievements_list.order_by('-quantity')

    has_achievement = False
    for achievement in correct_exercise_achievements_list:
        if user_corrected_exercise_quantity >= achievement.quantity:
            logger.info("Verifying if user: " + user.username + " has achievement: " + achievement.name)
            has_achievement = check_if_user_has_achievement(user, achievement)

            if has_achievement is False:
                unlock_achievement(user, achievement)
                break
            else:
                logger.info("The user already had unlocked this achievement!")
                break

        else:
            # Nothing to do.
            pass

    logger.info("There is no achievement to unlock!")


# Count all completed exercises for the current user.
def get_user_corrected_exercise_quantity(user):
    user_corrected_exercise_quantity = 0
    user_corrected_exercise_quantity = UserExercise.objects.filter(user=user, status=True).count()

    return user_corrected_exercise_quantity


# Find all achievements related to submited answers in topics and determine if the current user
# is able to unlock some of them.
def verify_submited_answers_achievement(user):
    logger.info("Verifying submited answers achievement!")
    user_submited_answers_quantity = get_user_submited_answers_quantity(user)

    # List of achievements that have the same type(submited answers).
    submited_answers_achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.SUBMITED_ANSWERS_ACHIEVEMENTS)

    # The list of achievements must be ordered by the biggest quantity of correct exercises.
    submited_answers_achievements_list = submited_answers_achievements_list.order_by('-quantity')

    has_achievement = False
    for achievement in submited_answers_achievements_list:
        if user_submited_answers_quantity >= achievement.quantity:
            logger.info("Verifying if user: " + user.username + " has achievement: " + achievement.name)
            has_achievement = check_if_user_has_achievement(user, achievement)

            if has_achievement is False:
                unlock_achievement(user, achievement)
                break
            else:
                logger.info("The user already had unlocked this achievement!")
                break

        else:
            # Nothing to do.
            pass

    logger.info("There is no achievement to unlock!")


# Count all submited answers for the current user.
def get_user_submited_answers_quantity(user):
    user_submited_answers_quantity = 0
    user_submited_answers_quantity = Answer.objects.filter(user=user).count()

    return user_submited_answers_quantity


# Verifies if exists a relationship between the current user and the current achievement in database.
def check_if_user_has_achievement(user, achievement):
    try:
        UserAchievement.objects.get(user=user, achievement=achievement)
        has_achievement = True
    except UserAchievement.DoesNotExist:
        has_achievement = False

    return has_achievement


# Unlock the achievement creating a relationship between the current user
# and the current achievement in database.
def unlock_achievement(user, achievement):
    user_achievement = UserAchievement()
    user_achievement.update_or_creates(user, achievement)
    logger.info(user.username + " just unlocked achievement " + achievement.name)
