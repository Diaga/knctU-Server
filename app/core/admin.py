from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'title', 'avatar')}),
        (('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (('Important dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# User
admin.site.register(models.User, UserAdmin)

# Forum
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Comment)
admin.site.register(models.Reply)

# Chat
admin.site.register(models.ChatRoom)
admin.site.register(models.Message)
admin.site.register(models.MessageUser)
