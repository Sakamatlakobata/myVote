# Generated by Django 3.2.12 on 2022-10-15 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Messaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=128, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('district', models.IntegerField(blank=True, default=0, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=7, null=True)),
                ('street', models.CharField(blank=True, max_length=64, null=True)),
                ('owner', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messaging', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['subject'],
            },
        ),
    ]