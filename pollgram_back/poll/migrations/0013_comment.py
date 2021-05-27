# Generated by Django 3.1.7 on 2021-05-27 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0012_auto_20210527_2357'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('dislikes', models.ManyToManyField(related_name='disliked_comment', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='liked_comment', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='poll.comment')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='poll.poll')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
