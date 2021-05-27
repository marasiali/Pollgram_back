from django.contrib import admin

from poll.models import Poll, Choice, Image, File, Category

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(File)
admin.site.register(Image)
admin.site.register(Category)

# Register your models here.
