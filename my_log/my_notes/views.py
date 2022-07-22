from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView, TemplateView

from .forms import EntryForm, TopicForm
#
from .models import Entry, Topic

# My Class Based views.


class Index(TemplateView):
    template_name = "my_notes/index.html"


class Topics(TemplateView):
    template_name = "my_notes/topics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["themes"] = Topic.objects.order_by("date_added")
        return context


class Theme(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    template_name = "my_notes/topic.html"

    def get_context_data(self, topic_id, **kwargs):
        topic = get_object_or_404(Topic, id=topic_id)
        context = super().get_context_data(**kwargs)
        context["topic"] = topic
        context["entries"] = topic.topic.order_by("-date_added")
        return context


class NewTopic(LoginRequiredMixin, View):
    login_url = "/users/login/"
    form_class = TopicForm
    template_name = "my_notes/new_topic.html"

    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_theme = form.save(commit=False)
            new_theme.owner = request.user
            new_theme.save()
            return HttpResponseRedirect(reverse("my_notes:topics"))


class NewEntry(LoginRequiredMixin, View):
    login_url = "/users/login/"
    form_class = EntryForm
    template_name = "my_notes/new_entry.html"

    def get(self, request, topic_id):
        topic = Topic.objects.get(id=topic_id)
        if topic.owner != request.user:
            raise Http404("You can't add entries outside your own topics.")
        form = self.form_class()
        context = {"topic": topic, "form": form}
        return render(request, self.template_name, context)

    def post(self, request, topic_id):
        topic = Topic.objects.get(id=topic_id)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.topic = topic
            entry.owner = topic.owner
            entry.save()
            return HttpResponseRedirect(reverse("my_notes:topic", args=(topic_id,)))


class EditEntry(LoginRequiredMixin, View):
    login_url = "/users/login/"
    template_name = "my_notes/edit_entry.html"
    form_class = EntryForm

    def get(self, request, entry_id):
        entry = Entry.objects.get(id=entry_id)
        if entry.owner != request.user:
            raise Http404("You can edit your own entries only.")
        topic = entry.topic
        form = self.form_class(instance=entry)
        context = {"entry": entry, "topic": topic, "form": form}
        return render(request, self.template_name, context)

    def post(self, request, entry_id):
        entry = Entry.objects.get(id=entry_id)
        entry.date_added = datetime.now()
        form = self.form_class(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("my_notes:topic", args=(entry.topic.id,))
            )


class DeleteEntry(LoginRequiredMixin, DeleteView):
    login_url = "/users/login/"
    model = Entry

    def get_success_url(self):
        entry_id = self.kwargs["pk"]
        topic = Entry.objects.get(pk=entry_id).topic
        topic_id = topic.id
        return reverse_lazy("my_notes:topic", kwargs={"topic_id": topic_id})
