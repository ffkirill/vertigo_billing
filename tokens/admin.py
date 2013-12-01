from django.contrib import admin
from .models import Token, TokenReader

admin.site.register(Token)
admin.site.register(TokenReader)

