from django.test import TestCase
from django.contrib.auth.models import User
import time
from ..models import Topic, Entry


class TopicModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='123')
        user.save()
        Topic.objects.create(text='Test Topic', owner=user)

    def setUp(self) -> None:
        pass

    def test_text_label(self):
        topic = Topic.objects.get(pk=1)
        field_label = topic._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_date_added_label(self):
        topic = Topic.objects.get(pk=1)
        date_field_label = topic._meta.get_field('date_added').verbose_name
        self.assertEqual(date_field_label, 'date added')

    def test_text_max_length(self):
        topic = Topic.objects.get(pk=1)
        text_length = topic._meta.get_field('text').max_length
        self.assertEqual(text_length, 200)

    def test_check_owner(self):
        topic = Topic.objects.get(pk=1)
        self.assertEqual(str(topic.owner), 'testuser')

    def test_obj_name_is_text(self):
        topic = Topic.objects.get(pk=1)
        expected_obj_name = f"{topic.text}"
        self.assertEqual(expected_obj_name, str(topic))


class EntryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='123')
        user.save()
        topic = Topic.objects.create(text='Test Topic', owner=user)
        topic.save()
        time.sleep(0.01)
        Entry.objects.create(topic=topic, text='testtesttesttesttest', owner=user)

    def setUp(self) -> None:
        pass

    def test_text_label(self):
        entry = Entry.objects.get(pk=1)
        field_label = entry._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_topic_label(self):
        entry = Entry.objects.get(pk=1)
        field_label = entry._meta.get_field('topic').verbose_name
        self.assertEqual(field_label, 'topic')

    def test_entry_owner_is_topic_owner(self):
        entry = Entry.objects.get(pk=1)
        topic = Topic.objects.get(pk=1)
        self.assertEqual(entry.owner, topic.owner)

    def test_verbose_name_plural(self):
        entry = Entry.objects.get(pk=1)
        expected_verbose_name_plural = entry._meta.verbose_name_plural
        self.assertEqual(expected_verbose_name_plural, 'entries')

    def test_obj_name_is_text(self):
        entry = Entry.objects.get(pk=1)
        expected_obj_name = f"{entry.text[:50]}..."
        self.assertEqual(expected_obj_name, str(entry))

    def test_entry_date_added_after_topic_date_added(self):
        entry = Entry.objects.get(pk=1)
        topic = Topic.objects.get(pk=1)
        self.assertTrue(entry.date_added > topic.date_added)
