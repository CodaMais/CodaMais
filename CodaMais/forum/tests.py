# Django.
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.storage.fallback import FallbackStorage

# local Django.

from forum.models import (
    Topic, Answer
)
from user.models import User
from forum.views import (
    list_all_topics, show_topic,
    create_topic, delete_topic, delete_answer,
    best_answer, __show_choose_best_answer_button__,
    __show_delete_answer_button__, __show_lock_topic_button__,
    lock_topic,
)

# RESPONSE CODES.
REQUEST_SUCCEEDED = 200  # 200 is return with success response.

# 302 is the value returned from a HttpRequest status code when the URL was redirected.
REQUEST_REDIRECT = 302


class TestTopicCreation(TestCase):
    topic = Topic()
    user = User()

    def setUp(self):
        self.topic.title = 'Basic Topic'
        self.topic.subtitle = 'How test in Django'
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.topic.description = '<p>Text Basic Exercise.</p>'
        self.user.save()

    def test_str_is_correct(self):
        self.topic.author = self.user
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(str(topic_database), str(self.topic))

    def test_if_topic_is_saved_database(self):
        self.topic.author = self.user
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database, self.topic)

    def test_topic_get_title(self):
        self.topic.author = self.user
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database.title, self.topic.title)

    def test_topic_get_subtitle(self):
        self.topic.author = self.user
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database.subtitle, self.topic.subtitle)

    def test_topic_get_author(self):
        self.topic.author = self.user
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(str(topic_database.author), str(self.topic.author))

    def test_topic_get_description(self):
        self.topic.author = self.user
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database.description, self.topic.description)


class TestRequestTopic(TestCase):

        topic = Topic()
        user = User()

        def setUp(self):
            self.user.email = "user@user.com"
            self.user.first_name = "TestUser"
            self.user.username = "Username"
            self.user.is_active = True
            self.user.set_password('userpassword')
            self.user.save()

            self.user_wrong = User()
            self.user_wrong.email = "wronguser@wronguser.com"
            self.user_wrong.first_name = "WrongUser"
            self.user_wrong.username = "WrongUser"
            self.user_wrong.is_active = True

            self.topic.title = 'Basic Topic'
            self.topic.subtitle = 'How test in Django'
            self.topic.author = self.user
            self.topic.description = '<p>Text Basic Exercise.</p>'
            self.topic.locked = False

            self.factory = RequestFactory()
            self.wrong_author = 'User'
            self.topic_creation_form = {
                'title': self.topic.title,
                'subtitle': self.topic.subtitle,
                'description': self.topic.description,
            }
            self.wrong_topic_creation_form = self.topic_creation_form

        def test_list_all_topics(self):
            request = self.factory.get('/forum/topics/')
            response = list_all_topics(request)
            self.assertEqual(response.status_code, REQUEST_SUCCEEDED)

        def test_show_topic(self):
            self.topic.save()
            request = self.factory.get('/forum/topics/1/')
            request.user = self.user
            response = show_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_SUCCEEDED)

        def test_show_topic_when_topic_is_not_deletable(self):
            self.topic.save()

            self.user_wrong.save()
            request = self.factory.get('/forum/topics/1/')
            request.user = self.user_wrong
            response = show_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_SUCCEEDED)

        # def test_show_topic_when_topic_is_not_deletable(self):
        #     self.topic.author.username = self.wrong_author.username
        #     self.topic.save()
        #     request = self.factory.get('/forum/topics/1/')
        #     request.user = self.user
        #     response = show_topic(request, self.topic.id)
        #     self.assertEqual(response.status_code, REQUEST_SUCCEEDED)

        def test_show_topic_if_topic_does_not_exit(self):
            request = self.factory.get('/forum/topics/1/')
            request.user = self.user
            response = show_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

        def test_create_topic(self):
            request = self.factory.post('/forum/newtopic/', self.topic_creation_form)

            # This is necessary to test with messages.
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)

            request.user = self.user
            response = create_topic(request)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

        def test_create_topic_with_invalid_form(self):
            self.wrong_topic_creation_form['title'] = ' '
            request = self.factory.post('/forum/newtopic/', self.wrong_topic_creation_form)
            request.user = self.user
            response = create_topic(request)
            self.assertEqual(response.status_code, REQUEST_SUCCEEDED)

        def test_if_user_can_delete_topic(self):
            self.topic.save()
            request = self.factory.get('/forum/deletetopic/1/', follow=True)
            request.user = self.user
            response = delete_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

        def test_if_user_cant_delete_topic(self):
            self.topic.author.username = self.wrong_author
            self.topic.save()
            request = self.factory.get('/forum/deletetopic/1/', follow=True)
            request.user = self.user
            response = delete_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

        def test_delete_topic_which_does_not_exit(self):
            request = self.factory.get('/forum/deletetopic/1/', follow=True)
            request.user = self.user
            response = delete_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

        def test_show_lock_topic_button_when_topic_isnt_lockable(self):
            self.user_wrong.save()
            self.topic.save()
            lockable_topic = __show_lock_topic_button__(self.topic, self.user_wrong)
            self.assertFalse(lockable_topic)

        def test_show_lock_topic_button_when_topic_is_lockable(self):
            self.topic.save()
            lockable_topic = __show_lock_topic_button__(self.topic, self.user)
            self.assertTrue(lockable_topic)

        def test_show_lock_topic_button_when_topic_is_already_locked(self):
            topic = self.topic
            topic.locked = True
            topic.save()
            lockable_topic = __show_lock_topic_button__(topic, self.user)
            self.assertFalse(lockable_topic, False)

        def test_show_lock_topic_button_when_topic_is_null(self):
            topic = None
            try:
                __show_lock_topic_button__(topic, self.user)
            except AssertionError:
                self.assertTrue(True)

        def test_show_lock_topic_button_when_user_is_null(self):
            self.topic.save()
            user = None
            try:
                __show_lock_topic_button__(self.topic, user)
            except AssertionError:
                self.assertTrue(True)

        def test_lock_topic_when_topic_is_lockable(self):
            self.topic.save()
            request = self.factory.get('/forum/locktopic/' + str(self.topic.id), follow=True)
            request.user = self.user
            response = lock_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

            locked_topic = Topic.objects.get(id=self.topic.id)

            self.assertTrue(locked_topic.locked)

        def test_lock_topic_when_topic_doesnt_exist(self):
            request = self.factory.get('/forum/locktopic/' + str(self.topic.id), follow=True)
            request.user = self.user
            lock_topic(request, self.topic.id)
            self.assertRaises(ObjectDoesNotExist)

        def test_lock_topic_when_user_cant_lock(self):
            self.user_wrong.save()
            self.topic.save()
            request = self.factory.get('/forum/locktopic/' + str(self.topic.id), follow=True)
            request.user = self.user_wrong
            response = lock_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

        def test_lock_topic_when_user_is_staff_lock(self):
            user = self.user_wrong
            user.is_staff = True
            user.save()
            self.topic.save()
            request = self.factory.get('/forum/locktopic/' + str(self.topic.id), follow=True)
            request.user = user
            response = lock_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

            locked_topic = Topic.objects.get(id=self.topic.id)

            self.assertTrue(locked_topic.locked)


class TestAnswerCreation(TestCase):
    answer = Answer()
    topic = Topic()
    user = User()
    user_topic = User()

    def setUp(self):
        self.answer.description = "<p>Description answer.</p>"
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.user_topic.email = "usertopic@user.com"
        self.user_topic.first_name = "TestUser"
        self.user_topic.username = "UserTopic"
        self.user_topic.is_active = True
        self.user_topic.save()
        self.topic.title = 'Basic Topic'
        self.topic.subtitle = 'How test in Django'
        self.topic.author = self.user_topic
        self.topic.description = '<p>Text Basic Exercise.</p>'
        self.user.set_password('userpassword')
        self.user.save()
        self.topic.save()

    def test_if_answer_is_saved_database(self):
        self.answer.user = self.user
        self.answer.topic = self.topic
        self.answer.save()
        answer_database = Answer.objects.get(id=self.answer.id)
        self.assertEqual(str(answer_database), str(self.answer))

    def test_if_creates_answer(self):
        self.answer.creates_answer(self.user, self.topic, self.answer.description)
        answer_database = Answer.objects.get(id=self.answer.id)
        self.assertEqual(str(answer_database), str(self.answer))

    def test_answer_get_description(self):
        self.answer.creates_answer(self.user, self.topic, self.answer.description)
        answer_database = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer_database.description, self.answer.description)

    def test_answer_get_date(self):
        self.answer.creates_answer(self.user, self.topic, self.answer.description)
        answer_database = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer_database.date_answer, self.answer.date_answer)

    def test_answer_get_user(self):
        self.answer.creates_answer(self.user, self.topic, self.answer.description)
        answer_database = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer_database.user, self.answer.user)

    def test_answer_get_topic(self):
        self.answer.creates_answer(self.user, self.topic, self.answer.description)
        answer_database = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer_database.topic, self.answer.topic)


class TestAnswerTopic(TestCase):
    answer = Answer()
    topic = Topic()
    user = User()
    user_topic = User()

    def setUp(self):
        self.answer.description = "<p>Description answer.</p>"
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.user_topic.email = "usertopic@user.com"
        self.user_topic.first_name = "TestUser"
        self.user_topic.username = "UserTopic"
        self.user_topic.is_active = True
        self.user_topic.save()
        self.topic.title = 'Basic Topic'
        self.topic.subtitle = 'How test in Django'
        self.topic.description = '<p>Text Basic Exercise.</p>'
        self.topic.author = self.user_topic
        self.factory = RequestFactory()
        self.user.set_password('userpassword')
        self.user.save()
        self.topic.save()
        self.wrong_user = 'User'
        self.answer_creation_form = {
            'description': self.answer.description,
        }

    def test_answer_topic(self):
        request = self.factory.post('/forum/topics/1/', self.answer_creation_form)
        request.user = self.user
        response = show_topic(request, 1)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)

    def test_list_all_answer(self):
        list_answers = self.topic.answers()
        self.assertEqual(len(list_answers), 0)

    def list_all_answer_except_best_answer(self):
        self.answer.user = self.user
        self.answer.topic = self.topic
        self.answer.save()

        self.topic.best_answer = self.answer
        self.topic.save()

        list_answers = self.topic.answers()

        self.assertEqual(len(list_answers), 0)

    def test_if_user_can_delete_answer(self):
        self.answer.user = self.user
        self.answer.topic = self.topic
        self.answer.save()
        request = self.factory.get('/forum/deleteanswer/1/', follow=True)
        request.user = self.user
        response = delete_answer(request, self.answer.id)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)
        self.assertEqual(response.url, '/en/forum/topics/1/')

    def test_delete_answer_which_does_not_exit(self):
        self.answer.user = self.user
        self.answer.topic = self.topic
        self.answer.save()
        request = self.factory.get('/forum/deleteanswer/12/', follow=True)
        request.user = self.user
        response = delete_answer(request, 12)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)

    def test_if_user_cant_delete_answer(self):
        self.answer.user.username = self.wrong_user
        self.answer.topic = self.topic
        self.answer.save()
        request = self.factory.get('/forum/deleteanswer/1/', follow=True)
        request.user = self.user
        response = delete_answer(request, self.answer.id)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)
        self.assertEqual(response.url, '/en/forum/topics/1/')

    def test_if_user_can_see_delete_answer_button(self):
        self.answer.user = self.user
        self.answer.topic = self.topic
        self.answer.save()
        answers = Answer.objects.filter(topic=self.answer.topic)
        not_deletable_answer = []
        not_deletable_answer.append(True)
        deletable_answers = __show_delete_answer_button__(answers, self.topic, self.user.username)
        self.assertEqual(deletable_answers, not_deletable_answer)

    def test_if_user_cant_see_delete_answer_button(self):
        self.answer.user = self.user
        self.answer.topic = self.topic
        self.answer.save()
        answers = Answer.objects.filter(topic=self.topic)
        not_deletable_answer = []
        not_deletable_answer.append(False)
        deletable_answers = __show_delete_answer_button__(answers, self.topic, self.wrong_user)
        self.assertEqual(deletable_answers, not_deletable_answer)

    def test_if_user_can_see_choose_best_answer_button(self):
        topic_author = self.topic.author
        current_user = topic_author
        choose_best_answer = __show_choose_best_answer_button__(topic_author, current_user)
        self.assertEqual(choose_best_answer, True)

    def test_if_user_cant_see_choose_best_answer_button(self):
        topic_author = self.topic.author
        current_user = self.user
        choose_best_answer = __show_choose_best_answer_button__(topic_author, current_user)
        self.assertEqual(choose_best_answer, False)

    def test_if_topic_author_cant_choose_an_inexistent_answer(self):
        request = self.factory.get('/forum/best_answer/1/')
        request.user = self.user
        response = best_answer(request, self.answer.id)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)
        self.assertEqual(response.url, '/en/forum/topics/')

    def test_if_topic_author_can_choose_best_answer(self):
        self.answer.user = self.user
        self.answer.topic = self.topic
        self.answer.save()
        request = self.factory.get('/forum/best_answer/1/')
        request.user = self.topic.author
        response = best_answer(request, self.answer.id)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)
        self.assertEqual(response.url, '/en/forum/topics/1/')
