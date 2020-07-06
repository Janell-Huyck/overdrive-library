from django.db import models
from django.contrib.auth.models import AbstractUser

from .helpers import makenumber


class CustomUser(AbstractUser):
    library_card_number = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=254)
    signup_date = models.DateField(auto_now_add=True, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    display_name = models.CharField(max_length=50, unique=True)
    REQUIRED_FIELDS = ['email', 'display_name']

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.library_card_number:
            self.library_card_number = makenumber()
        super(CustomUser, self).save(**args, **kwargs)


"""
Custom_User

display_name: charfield
library card number : integer field
password :  Charfield, password widget
signup date: datefield
email: email field
Is an admin: Boolean

"""
