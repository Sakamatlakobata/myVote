# Generated by Django 3.2.12 on 2022-09-10 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20220825_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='bill_id',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='type',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
