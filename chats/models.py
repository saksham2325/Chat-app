from email import message
from pyexpat import model
from tokenize import group
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from chats import constants as chats_constants
from chats.manager import UserManager
from common import models as common_models


class User(AbstractUser, common_models.Timestamp):
    """
    This is the User Table which extracts from AbstractUser and it inherits TimeStamp model to keep an record for created and updated and we define create_auth_token which will generate authentication token as soon as the user will save in database.
    """
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=chats_constants.FIRST_NAME_LAST_NAME_MAX_LENGTH)
    last_name = models.CharField(
        max_length=chats_constants.FIRST_NAME_LAST_NAME_MAX_LENGTH, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Group(common_models.Timestamp):
    title = models.CharField(max_length=chats_constants.GROUP_TITLE_LENGTH)
    #Here we can also add the creator column which will be an Foreign Key from user table
 
    def __str__(self):
        return self.title


class UserGroup(common_models.Timestamp):
    ADMIN = 0
    CREATOR = 1
    NORMAL_USER = 2
    ROLE_CHOICE = [
        (ADMIN, 'Admin'),
        (CREATOR, 'Creator'),
        (NORMAL_USER, 'Normal_user')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, default=NORMAL_USER)

    def __str__(self):
        return "{}->{}".format(self.user, self.group)


"""class Message(common_models.Timestamp):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.CharField(max_length=chats_constants.MESSAGE_LENGTH)"""
