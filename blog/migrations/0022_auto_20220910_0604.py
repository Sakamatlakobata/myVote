# Generated by Django 3.2.12 on 2022-09-10 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20220910_0604'),
        ('events', '0007_auto_20220906_1145'),
        ('blog', '0021_rename_post_date_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='bill',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.bill'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='event',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.event'),
        ),
    ]
