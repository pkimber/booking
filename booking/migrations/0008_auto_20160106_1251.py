# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20150104_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='booking')),
            ],
            options={
                'verbose_name_plural': 'Rooms',
                'verbose_name': 'Room',
                'ordering': ('title',),
            },
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name_plural': 'Locations', 'verbose_name': 'Location', 'ordering': ('title',)},
        ),
        migrations.AddField(
            model_name='bookingsettings',
            name='display_rooms',
            field=models.BooleanField(default=False, help_text="Does this project use 'Rooms'?"),
        ),
        migrations.AddField(
            model_name='category',
            name='per_day_booking',
            field=models.BooleanField(default=True, help_text='Is the minimum booking period one day?'),
        ),
        migrations.AlterField(
            model_name='location',
            name='url_map',
            field=models.URLField(null=True, blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='room',
            name='location',
            field=models.ForeignKey(null=True, to='booking.Location', blank=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(null=True, to='booking.Room', blank=True),
        ),
    ]
