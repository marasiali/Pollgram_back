# Generated by Django 3.1.7 on 2021-05-27 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0010_auto_20210527_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('order',), 'verbose_name': 'Categorie'},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poll',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polls', to='poll.category'),
        ),
    ]
