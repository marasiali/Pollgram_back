from django.contrib import admin

from poll.models import Poll, Choice, Image, File, Category, Comment

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(File)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Comment)

# Register your models here.
