from django.urls import path

from . import views

app_name = "my_notes"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("topics/", views.Topics.as_view(), name="topics"),
    path("topic/<int:topic_id>", views.Theme.as_view(), name="topic"),
    path("new_topic/", views.NewTopic.as_view(), name="new_topic"),
    path("new_entry/<int:topic_id>", views.NewEntry.as_view(), name="new_entry"),
    path("edit_entry/<int:entry_id>", views.EditEntry.as_view(), name="edit_entry"),
    path("<int:pk>/delete/", views.DeleteEntry.as_view(), name="delete_entry"),
]
