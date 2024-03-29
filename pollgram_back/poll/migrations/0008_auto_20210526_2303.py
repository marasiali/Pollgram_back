# Generated by Django 3.1.7 on 2021-05-26 18:33

from django.db import migrations, models
import poll.models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0007_auto_20210525_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, max_length=250, null=True, upload_to=poll.models.File.get_upload_file_url),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, max_length=250, null=True, upload_to=poll.models.Image.get_upload_file_url),
        ),
    ]
