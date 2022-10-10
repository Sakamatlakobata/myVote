# Generated by Django 3.2.12 on 2022-09-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='district',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='venue',
            name='zipcode',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]