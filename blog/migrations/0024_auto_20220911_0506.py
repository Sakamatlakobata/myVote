# Generated by Django 3.2.12 on 2022-09-11 05:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20220911_0506'),
        ('events', '0007_auto_20220906_1145'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0023_alter_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='bill',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.bill'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='event',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='events.event'),
        ),
    ]
