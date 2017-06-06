# standard library
import logging

# Local Django
from achievement import constants
from exercise.models import UserExercise
from django.contrib import messages
from forum.models import Answer
from achievement.models import (
    Achievement, UserAchievement
)

# Loggers Config
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Find all achievements related to corrected exercises and determine if the current user
# is able to unlock some of them.
def verify_correct_exercise_achievement(user, request):
    logger.debug("Verifying correct exercise achievement.")

    user_corrected_exercise_quantity = get_user_corrected_exercise_quantity(user)

    # List of achievements that have the same type(correct exercise).
    correct_exercise_achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.CORRECT_EXERCISE_ACHIEVEMENTS)

    # The list of achievements must be ordered by the biggest quantity of correct exercises.
    correct_exercise_achievements_list = correct_exercise_achievements_list.order_by('-quantity')

    # Verify in fact wich achievement of the specific type achievements list the user should get.
    check_achievement_user_should_get(user, user_corrected_exercise_quantity,
                                      correct_exercise_achievements_list, request)

    logger.debug("Ending verifycation of correct exercise achievement.")


# Count all completed exercises for the current user.
def get_user_corrected_exercise_quantity(user):
    assert user is not None, "User not logged in."

    user_corrected_exercise_quantity = 0
    user_corrected_exercise_quantity = UserExercise.objects.filter(user=user, status=True).count()

    assert user_corrected_exercise_quantity >= 0, "Invalid number of user corrected exercises"

    return user_corrected_exercise_quantity


# Find all achievements related to submited answers in topics and determine if the current user
# is able to unlock some of them.
def verify_submited_answers_achievement(user, request):
    logger.debug("Verifying submited answers achievement.")

    user_submited_answers_quantity = get_user_submited_answers_quantity(user)

    # List of achievements that have the same type(submited answers).
    submited_answers_achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.SUBMITED_ANSWERS_ACHIEVEMENTS)

    # The list of achievements must be ordered by the biggest quantity of correct exercises.
    submited_answers_achievements_list = submited_answers_achievements_list.order_by('-quantity')

    # Verify in fact wich achievement of the specific type achievements list the user should get.
    check_achievement_user_should_get(user, user_submited_answers_quantity,
                                      submited_answers_achievements_list, request)

    logger.debug("Ending verifycation of submited answers achievement.")


# Count all submited answers for the current user.
def get_user_submited_answers_quantity(user):
    assert user is not None, "User not logged in."

    user_submited_answers_quantity = 0
    user_submited_answers_quantity = Answer.objects.filter(user=user).count()

    assert user_submited_answers_quantity >= 0, "Invalid number of user submited answers"

    return user_submited_answers_quantity


# Find all achievements related to score and determine if the current user is able to unlock some of them.
# This method should be called everywhere user is scored.
def verify_score_achievement(user, request):
    logger.debug("Verifying score achievement.")

    # List of achievements that have the same type(score).
    score_achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.SCORE_ACHIEVEMENTS)

    # The list of achievements must be ordered by the biggest quantity of score.
    score_achievements_list = score_achievements_list.order_by('-quantity')

    score = user.score
    # Verify in fact wich achievement of the specific type achievements list the user should get.
    check_achievement_user_should_get(user, score, score_achievements_list, request)

    logger.debug("Ending verifycation of score achievement.")


# Find all achievements related to submited exercises in topics and determine if the current user
# is able to unlock some of them.
def verify_submited_exercises_achievement(user, request):
    logger.debug("Verifying submited exercise achievement.")

    user_submited_exercises_quantity = get_user_submited_exercises_quantity(user)

    # List of achievements that have the same type(submited exercises).
    submited_exercise_achievements_list = Achievement.objects.filter(
                                    achievement_type=constants.SUBMITED_EXERCISE_ACHIEVEMENTS)

    # The list of achievements must be ordered by the biggest quantity of correct exercises.
    submited_exercise_achievements_list = submited_exercise_achievements_list.order_by('-quantity')

    # Verify in fact wich achievement of the specific type achievements list the user should get.
    check_achievement_user_should_get(user, user_submited_exercises_quantity,
                                      submited_exercise_achievements_list, request)

    logger.debug("Ending verifycation of submited exercises achievement.")


# Count all submissions of all exercises that the user submited, correct or not.
def get_user_submited_exercises_quantity(user):
    assert user is not None, "User not logged in."

    submited_exercises_list = UserExercise.objects.filter(user=user)
    user_submited_exercises_quantity = 0

    for submited_exercise in submited_exercises_list:
        user_submited_exercises_quantity += submited_exercise.number_submission

    assert user_submited_exercises_quantity >= 0, "Invalid number of user submited exercise"

    return user_submited_exercises_quantity


# Verifies if exists a relationship between the current user and the current achievement in database.
def check_if_user_has_achievement(user, achievement):
    assert user is not None, "User not logged in."
    assert achievement is not None, "Achievement does not exist."

    try:
        UserAchievement.objects.get(user=user, achievement=achievement)
        has_achievement = True
    except UserAchievement.DoesNotExist:
        has_achievement = False

    return has_achievement


# Unlock the achievement creating a relationship between the current user
# and the current achievement in database.
def unlock_achievement(user, achievement):
    assert user is not None, "User not logged in."
    assert achievement is not None, "Achievement does not exist."

    user_achievement = UserAchievement()
    user_achievement.update_or_creates(user, achievement)

    logger.info(user.username + " just unlocked achievement " + achievement.name)


# Verify which achievement the user should get or not, based on the specific quantity of
# something that the achievement is related.
def check_achievement_user_should_get(user, specific_user_quantity, achievements_list, request):
    assert user is not None, "User not logged in."
    assert achievements_list is not None, "Doesn't exist achievements in this Achievements list"
    assert specific_user_quantity >= 0, "Invalid number of specific user quantity."

    has_achievement = False
    for achievement in achievements_list:
        if specific_user_quantity >= achievement.quantity:
            logger.info("Verifying if user: " + user.username + " has achievement: " + achievement.name)
            has_achievement = check_if_user_has_achievement(user, achievement)

            if has_achievement is False:
                unlock_achievement(user, achievement)
                messages.success(request, "Você desbloqueou a conquista " + achievement.name)
                break
            else:
                logger.info("The user: " + user.username + " already had unlocked this achievement.")
                break

        else:
            # Nothing to do.
            pass

    logger.info("There is no achievement to unlock for the user: " + user.username + ".")
