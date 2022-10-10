# Generated by Django 3.2.12 on 2022-09-07 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20220825_0528'),
        ('events', '0007_auto_20220906_1145'),
        ('blog', '0019_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bill',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.bill'),
        ),
        migrations.AddField(
            model_name='post',
            name='event',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
    ]