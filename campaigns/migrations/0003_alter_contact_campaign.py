# Generated by Django 3.2.12 on 2022-10-09 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20221007_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='campaign',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact', to='campaigns.campaign'),
        ),
    ]