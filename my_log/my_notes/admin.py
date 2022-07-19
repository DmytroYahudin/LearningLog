from django.contrib import admin
from .models import Topic, Entry

# My registered models.
admin.site.register(Topic)
admin.site.register(Entry)
