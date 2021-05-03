from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import FollowRelationship

class CutsomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
            ('Profile', {'fields': (
                                'avatar',
                                'cover',
                                'bio',
                                'is_public',
                                'is_verified',
            )}),
    )
admin.site.register(get_user_model(), CutsomUserAdmin)
admin.site.register(FollowRelationship)