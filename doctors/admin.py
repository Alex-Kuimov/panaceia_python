from django.contrib import admin

from .models import Meeting, Calendar, Review

admin.site.register(Meeting)
admin.site.register(Calendar)
admin.site.register(Review)
