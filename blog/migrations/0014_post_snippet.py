# Generated by Django 3.2.12 on 2022-08-17 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='snippet',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
