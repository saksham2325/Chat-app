from django.contrib import admin

from chats import models as chats_models

admin.site.register(chats_models.User)
admin.site.register(chats_models.Group)
admin.site.register(chats_models.UserGroup)
