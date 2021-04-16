from django.contrib import admin
from .models import UserProfile, FollowRelationship


admin.site.register(UserProfile)
admin.site.register(FollowRelationship)