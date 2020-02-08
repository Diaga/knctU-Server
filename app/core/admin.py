from django.contrib import admin

from . import models

# User
admin.site.register(models.User)

# Forum
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Comment)
admin.site.register(models.Reply)
