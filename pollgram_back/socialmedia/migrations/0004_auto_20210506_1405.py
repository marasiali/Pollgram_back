# Generated by Django 3.1.7 on 2021-05-06 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0003_auto_20210506_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followrelationship',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows_relationships', to=settings.AUTH_USER_MODEL, verbose_name='From'),
        ),
        migrations.AlterField(
            model_name='followrelationship',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_relationships', to=settings.AUTH_USER_MODEL, verbose_name='To'),
        ),
        migrations.AlterField(
            model_name='user',
            name='followings',
            field=models.ManyToManyField(related_name='followers', through='socialmedia.FollowRelationship', to=settings.AUTH_USER_MODEL),
        ),
    ]