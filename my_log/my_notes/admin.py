from django.contrib import admin

from .models import Entry, Topic

# My registered models.
admin.site.register(Topic)
admin.site.register(Entry)
