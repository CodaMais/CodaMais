# Django.
from django.test import TestCase
from django.test.client import RequestFactory

# local Django.

from forum.models import Topic
from user.models import User
from forum.views import (
    list_all_topics, show_topic, create_topic, delete_topic,
)

# RESPONSE CODES.
REQUEST_SUCCEEDED = 200  # 200 is return with success response.

# 302 is the value returned from a HttpRequest status code when the URL was redirected.
REQUEST_REDIRECT = 302


class TestTopicCreation(TestCase):
    topic = Topic()

    def setUp(self):
        self.topic.title = 'Basic Topic'
        self.topic.subtitle = 'How test in Django'
        self.topic.author = 'User'
        self.topic.description = '<p>Text Basic Exercise.</p>'

    def test_str_is_correct(self):
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(str(topic_database), str(self.topic))

    def test_if_topic_is_saved_database(self):
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database, self.topic)

    def test_topic_get_title(self):
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database.title, self.topic.title)

    def test_topic_get_subtitle(self):
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database.subtitle, self.topic.subtitle)

    def test_topic_get_author(self):
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database.author, self.topic.author)

    def test_topic_get_description(self):
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
            self.topic.title = 'Basic Topic'
            self.topic.subtitle = 'How test in Django'
            self.topic.author = 'Username'
            self.topic.description = '<p>Text Basic Exercise.</p>'
            self.factory = RequestFactory()
            self.user.set_password('userpassword')
            self.user.save()
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
            self.topic.author = self.wrong_author
            self.topic.save()
            request = self.factory.get('/forum/topics/1/')
            request.user = self.user
            response = show_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_SUCCEEDED)

        def test_show_topic_if_topic_does_not_exit(self):
            request = self.factory.get('/forum/topics/1/')
            request.user = self.user
            response = show_topic(request, self.topic.id)
            self.assertEqual(response.status_code, REQUEST_REDIRECT)
            self.assertEqual(response.url, '/en/forum/topics/')

        def test_create_topic(self):
            request = self.factory.post('/forum/newtopic/', self.topic_creation_form)
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
            self.topic.author = self.wrong_author
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
