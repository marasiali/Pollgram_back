from django.contrib import admin

from poll.models import Poll, Vote, Choice

admin.site.register(Poll)
admin.site.register(Vote)
admin.site.register(Choice)

# Register your models here.
