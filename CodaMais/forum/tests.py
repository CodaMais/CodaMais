# Django.
from django.test import TestCase
from django.test.client import RequestFactory

# local Django.
from forum import constants
from forum.models import Topic
from forum.views import list_all_topics, show_topic


class TestTopicCreation(TestCase):
    topic = Topic()

    def setUp(self):
        self.topic.title = 'Basic Topic'
        self.topic.subtilte = 'How test in Django'
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

    def test_topic_get_subtilte(self):
        self.topic.save()
        topic_database = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic_database.subtilte, self.topic.subtilte)

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

        def setUp(self):
            self.topic.title = 'Basic Topic'
            self.topic.subtilte = 'How test in Django'
            self.topic.author = 'User'
            self.topic.description = '<p>Text Basic Exercise.</p>'
            self.factory = RequestFactory()

        def test_list_all_topics(self):
            request = self.factory.get('/forum')
            response = list_all_topics(request)
            self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)

        def test_show_topic(self):
            self.topic.save()
            request = self.factory.get('/forum')
            response = show_topic(request, self.topic.id)
            self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)
