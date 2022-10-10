# Generated by Django 3.2.12 on 2022-09-06 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20220906_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='district',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='venue',
            name='district1',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='venue',
            name='zipcode1',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]