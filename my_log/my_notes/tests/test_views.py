from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Topic, Entry
from ..forms import TopicForm, EntryForm


class IndexViewTest(TestCase):

    def test_index_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_index_view_url_accessible_by_name(self):
        response = self.client.get(reverse('my_notes:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_right_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'my_notes/index.html')


class TopicsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='123')
        user.save()
        number_of_topics = 10
        for topic in range(number_of_topics):
            Topic.objects.create(text=f'Topic#{topic}', owner=user)

    def test_topics_view_url(self):
        response = self.client.get('/topics/')
        self.assertEqual(response.status_code, 200)

    def test_topics_view_url_accessible_by_name(self):
        response = self.client.get(reverse('my_notes:topics'))
        self.assertEqual(response.status_code, 200)

    def test_topics_view_uses_right_template(self):
        response = self.client.get('/topics/')
        self.assertTemplateUsed(response, 'my_notes/topics.html')

    def test_topics_view_context(self):
        response = self.client.get('/topics/')
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(len(response.context_data['themes']), 10)
        self.assertTrue(list(response.context_data['themes']) == list(Topic.objects.order_by('date_added')))


class ThemeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='testuser1', password='123')
        user1.save()
        user2 = User.objects.create_user(username='testuser2', password='345')
        user2.save()
        number_of_topics = 10
        for topic in range(number_of_topics):
            if topic % 2 == 0:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user1)
                theme.save()
                entry = Entry.objects.create(topic=theme, text=f'test entry {topic}', owner=user1)
                entry.save()
            else:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user2)
                theme.save()
                entry = Entry.objects.create(topic=theme, text=f'test entry {topic}', owner=user2)
                entry.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_notes:topic', kwargs={'topic_id': 1}))
        self.assertRedirects(response, '/users/login/?next=/topic/1')

    def test_logged_user_gets_correct_template(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:topic', kwargs={'topic_id': 1}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_notes/topic.html')

    def test_topic_view_context(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:topic', kwargs={'topic_id': 1}))
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(str(response.context_data['topic']), str(Topic.objects.get(pk=1)))
        self.assertEqual(len(response.context_data['entries']), 1)
        self.assertTrue(response.context_data['entries'][0] == Entry.objects.get(pk=1))

    def test_for_wrong_topic_id(self):
        self.client.login(username='testuser1', password='123')
        last_id = Topic.objects.latest('id').pk
        response = self.client.get(reverse('my_notes:topic', kwargs={'topic_id': last_id + 1}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')


class NewTopicViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='testuser1', password='123')
        user1.save()
        user2 = User.objects.create_user(username='testuser2', password='345')
        user2.save()
        number_of_topics = 10
        for topic in range(number_of_topics):
            if topic % 2 == 0:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user1)
                theme.save()
            else:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user2)
                theme.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_notes:new_topic'))
        self.assertRedirects(response, '/users/login/?next=/new_topic/')

    def test_logged_user_gets_correct_template(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:new_topic'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_notes/new_topic.html')

    def test_new_topic_view_context(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:new_topic'))
        self.assertIsInstance(response.context['form'], TopicForm)

    def test_post_method(self):
        self.client.login(username='testuser1', password='123')
        initial_number_of_topics = Topic.objects.count()
        new_topic = 'test topic'
        response = self.client.post(reverse('my_notes:new_topic'), {'text': new_topic, 'owner': 'testuser1'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_notes:topics'))
        current_number_of_topics = Topic.objects.count()
        self.assertEqual(current_number_of_topics, initial_number_of_topics + 1)
        added_topic = Topic.objects.last()
        self.assertEqual(added_topic.text, new_topic)
        self.assertEqual(str(added_topic.owner), 'testuser1')


class NewEntryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='testuser1', password='123')
        user1.save()
        user2 = User.objects.create_user(username='testuser2', password='345')
        user2.save()
        number_of_topics = 10
        for topic in range(number_of_topics):
            if topic % 2 == 0:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user1)
                theme.save()
                entry = Entry.objects.create(topic=theme, text=f'test entry {topic}', owner=user1)
                entry.save()
            else:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user2)
                theme.save()
                entry = Entry.objects.create(topic=theme, text=f'test entry {topic}', owner=user2)
                entry.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_notes:new_topic'))
        self.assertRedirects(response, '/users/login/?next=/new_topic/')

    def test_logged_user_gets_correct_template(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:new_entry', kwargs={'topic_id': 1}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_notes/new_entry.html')

    def test_new_entry_view_context(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:new_entry', kwargs={'topic_id': 1}))
        self.assertEqual(response.context['topic'], Topic.objects.get(pk=1))
        self.assertIsInstance(response.context['form'], EntryForm)

    def test_for_getting_404_code(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:new_entry', kwargs={'topic_id': 2}))
        self.assertEqual(response.status_code, 404)

    def test_post_method(self):
        self.client.login(username='testuser1', password='123')
        initial_number_of_entries = Entry.objects.count()
        entries = Entry.objects.filter(topic=Topic.objects.get(pk=1))
        initial_number_of_entries_in_topic = entries.count()
        new_entry = 'test entry'
        response = self.client.post(reverse('my_notes:new_entry', kwargs={'topic_id': 1}), {'text': new_entry, 'owner': 'testuser1'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_notes:topic', kwargs={'topic_id': 1}))
        updated_number_of_entries = Entry.objects.count()
        u_entries = Entry.objects.filter(topic=Topic.objects.get(pk=1))
        updated_number_of_entries_in_topic = u_entries.count()
        self.assertEqual(updated_number_of_entries, initial_number_of_entries + 1)
        self.assertEqual(updated_number_of_entries_in_topic, initial_number_of_entries_in_topic + 1)
        added_entry = Entry.objects.get(pk=updated_number_of_entries)
        self.assertEqual(added_entry.text, new_entry)
        self.assertEqual(str(added_entry.owner), 'testuser1')


class EditEntryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='testuser1', password='123')
        user1.save()
        user2 = User.objects.create_user(username='testuser2', password='345')
        user2.save()
        number_of_topics = 10
        for topic in range(number_of_topics):
            if topic % 2 == 0:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user1)
                theme.save()
                entry = Entry.objects.create(topic=theme, text=f'test entry {topic}', owner=user1)
                entry.save()
            else:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user2)
                theme.save()
                entry = Entry.objects.create(topic=theme, text=f'test entry {topic}', owner=user2)
                entry.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_notes:edit_entry', kwargs={'entry_id': 1}))
        self.assertRedirects(response, '/users/login/?next=/edit_entry/1')

    def test_logged_user_gets_correct_template(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:edit_entry', kwargs={'entry_id': 1}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_notes/edit_entry.html')

    def test_new_entry_view_context(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:edit_entry', kwargs={'entry_id': 1}))
        self.assertEqual(response.context['topic'], Topic.objects.get(pk=1))
        self.assertEqual(response.context['entry'], Entry.objects.get(pk=1))
        self.assertIsInstance(response.context['form'], EntryForm)

    def test_for_getting_404_code(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:edit_entry', kwargs={'entry_id': 2}))
        self.assertEqual(response.status_code, 404)

    def test_post_method(self):
        self.client.login(username='testuser1', password='123')
        initial_number_of_entries = Entry.objects.count()
        entries = Entry.objects.filter(topic=Topic.objects.get(pk=1))
        initial_number_of_entries_in_topic = entries.count()
        new_entry = 'test entry'
        response = self.client.post(reverse('my_notes:edit_entry', kwargs={'entry_id': 1}), {'text': new_entry, 'owner': 'testuser1'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_notes:topic', kwargs={'topic_id': 1}))
        updated_number_of_entries = Entry.objects.count()
        u_entries = Entry.objects.filter(topic=Topic.objects.get(pk=1))
        updated_number_of_entries_in_topic = u_entries.count()
        self.assertEqual(updated_number_of_entries, initial_number_of_entries)
        self.assertEqual(updated_number_of_entries_in_topic, initial_number_of_entries_in_topic)
        updated_entry = Entry.objects.get(pk=1)
        self.assertEqual(updated_entry.text, new_entry)
        self.assertEqual(str(updated_entry.owner), 'testuser1')


class DeleteEntryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='testuser1', password='123')
        user1.save()
        user2 = User.objects.create_user(username='testuser2', password='345')
        user2.save()
        number_of_topics = 10
        for topic in range(number_of_topics):
            if topic % 2 == 0:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user1)
                theme.save()
                entry = Entry.objects.create(topic=theme, text=f'test entry {topic}', owner=user1)
                entry.save()
            else:
                theme = Topic.objects.create(text=f'Topic#{topic}', owner=user2)
                theme.save()
                entry = Entry.objects.create(topic=theme, text=f'test entry {topic}', owner=user2)
                entry.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_notes:delete_entry', kwargs={'pk': 1}))
        self.assertRedirects(response, '/users/login/?next=/1/delete/')

    def test_logged_user_gets_correct_confirmation_template(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:delete_entry', kwargs={'pk': 1}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_notes/entry_confirm_delete.html')

    def test_delete_get_request(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my_notes:delete_entry', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'my_notes/entry_confirm_delete.html')
        self.assertContains(response, 'Are you sure')

    def test_delete_post_request(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.post(reverse('my_notes:delete_entry', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(response, reverse('my_notes:topic', kwargs={'topic_id': 1}), status_code=302)

    def test_number_of_entries_is_correct_after_delete_one(self):
        initial_number_of_entries = Entry.objects.count()
        self.client.login(username='testuser1', password='123')
        self.client.post(reverse('my_notes:delete_entry', kwargs={'pk': 1}), follow=True)
        current_number_of_entries = Entry.objects.count()
        self.assertEqual(initial_number_of_entries, current_number_of_entries + 1)