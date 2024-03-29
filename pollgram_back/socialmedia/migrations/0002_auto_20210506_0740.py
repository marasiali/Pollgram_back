# Generated by Django 3.1.7 on 2021-05-06 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followings',
            field=models.ManyToManyField(related_name='_user_followings_+', through='socialmedia.FollowRelationship', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followrelationship',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followings_relations', to=settings.AUTH_USER_MODEL, verbose_name='From'),
        ),
        migrations.AlterField(
            model_name='followrelationship',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers_relations', to=settings.AUTH_USER_MODEL, verbose_name='To'),
        ),
    ]
