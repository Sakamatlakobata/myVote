# Generated by Django 3.2.12 on 2022-08-29 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userextension_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='cell',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='userextension',
            name='office',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
