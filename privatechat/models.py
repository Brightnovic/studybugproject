from django.db import models

from base.models import User



class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_chats_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_chats_as_user2')

    def get_room_name(self):
        return f"Private Chat between {self.user1.username} and {self.user2.username}"

    def __str__(self):
        return self.get_room_name()


class PrivateMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[:50]







# Create your models here.
