from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
# Create your models here.


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class User(AbstractUser):

    class Meta:
        permissions = (
            ("only_email_validation", "can only use email validation"),
            ("only_translate_text", "Can only translate text"),
            ("do_both", "Can validate email and translate text"),
        )

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.id == 2:
            permission = Permission.objects.get(codename='only_email_validation')
            self.user_permissions.add(permission)
        if self.id == 3:
            permission = Permission.objects.get(codename='only_translate_text')
            self.user_permissions.add(permission)
        if self.id == 4:
            permission = Permission.objects.get(codename='do_both')
            self.user_permissions.add(permission)