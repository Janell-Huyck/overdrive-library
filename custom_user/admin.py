from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from custom_user.models import CustomUser


# help in this section is from
# https://testdriven.io/blog/django-custom-user-model/


class CustomUserAdmin(UserAdmin):
    list_display = ('display_name', 'email', 'library_card_number',
                    'signup_date', 'is_librarian')
    list_filter = ('display_name', 'email', 'library_card_number',
                   'signup_date', 'is_librarian')
    fieldsets = (
        (None, {'fields': ('display_name', 'email',
                           'is_librarian')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
