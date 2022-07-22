from django.test import TestCase

from ..forms import EntryForm, TopicForm
from ..models import Entry, Topic


class TopicFormTest(TestCase):
    def test_model_is_topic(self):
        form_data = {"text": "test"}
        form = TopicForm(data=form_data)
        self.assertEqual(form._meta.model, Topic)

    def test_form_for_entry_text(self):
        form_data = {"text": "test"}
        form = TopicForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_response_redirection(self):
        form_data = {"text": "test"}
        response = self.client.post("/new_topic/", data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_form_for_text_length_greater_then_200(self):
        form_data = {"text": "1234567890" * 20 + "1"}
        form = TopicForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_empty_entry_is_not_valid(self):
        form_data = {"text": ""}
        form = TopicForm(data=form_data)
        self.assertFalse(form.is_valid())


class EntryFormTest(TestCase):
    def test_model_is_entry(self):
        form_data = {"text": "test"}
        form = EntryForm(data=form_data)
        self.assertEqual(form._meta.model, Entry)

    def test_form_for_entry_text(self):
        form_data = {"text": "test"}
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_response_redirection(self):
        form_data = {"text": "test"}
        response = self.client.post("/new_entry/1", data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_form_empty_entry_is_not_valid(self):
        form_data = {"text": ""}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
