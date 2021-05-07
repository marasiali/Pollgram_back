from django.contrib import admin

from poll.models import Poll, Vote

admin.site.register(Poll)
admin.site.register(Vote)

# Register your models here.
