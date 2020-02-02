from django.contrib import admin

from . import models

# User
admin.site.register(models.User)

# Forum
admin.site.register(models.Question)
