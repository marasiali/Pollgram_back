from django.contrib import admin

from poll.models import Poll, Vote, Choice, Image, File

admin.site.register(Poll)
admin.site.register(Vote)
admin.site.register(Choice)
admin.site.register(File)
admin.site.register(Image)

# Register your models here.
