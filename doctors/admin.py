from django.contrib import admin

from .models import Meeting, Calendar

admin.site.register(Meeting)
admin.site.register(Calendar)