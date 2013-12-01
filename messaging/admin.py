from django.contrib import admin
from .models import Message, UsersMessages

admin.site.register(Message)
admin.site.register(UsersMessages)

