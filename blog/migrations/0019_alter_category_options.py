# Generated by Django 3.2.12 on 2022-08-29 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
    ]
