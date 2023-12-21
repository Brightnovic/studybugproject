from django.contrib import admin

# Register your models here.
from .models import PrivateChat,PrivateMessage

admin.site.register(PrivateChat)
admin.site.register(PrivateMessage)