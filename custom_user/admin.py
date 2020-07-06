from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from custom_user.models import CustomUser


# help in this section is from
# https://testdriven.io/blog/django-custom-user-model/

"""
    library_card_number = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=254)
    signup_date = models.DateField(auto_now_add=True, null=True, blank=True)
    is_librarian = models.BooleanField(default=False)
    display_name = models.CharField(max_length=50, unique=True)
    REQUIRED_FIELDS = ['email', 'display_name']
"""


class CustomUserAdmin(UserAdmin):
    list_display = ('display_name', 'email', 'library_card_number',
                    'signup_date', 'is_librarian')
    list_filter = ('display_name', 'email', 'library_card_number',
                   'signup_date', 'is_librarian')
    fieldsets = (
        (None, {'fields': ('display_name', 'email', 'library_card_number',
                           'signup_date', 'is_librarian')}),
        #  ("Permissions", {"fields": ("is_staff", "is_active")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
