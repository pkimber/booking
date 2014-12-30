# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=200)),
                ('promote', models.BooleanField(default=False)),
                ('routine', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('description',),
                'verbose_name_plural': 'Event types',
                'verbose_name': 'Event type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=200)),
                ('url', models.URLField(null=True, blank=True)),
                ('url_map', models.URLField(null=True, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('description',),
                'verbose_name_plural': 'Locations',
                'verbose_name': 'Location',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('slug',),
                'verbose_name_plural': 'Permissions',
                'verbose_name': 'Permission',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ('start_date', 'start_time'), 'verbose_name_plural': 'Bookings', 'verbose_name': 'Booking'},
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='to_date',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='from_date',
            new_name='start_date',
        ),
        migrations.AddField(
            model_name='booking',
            name='category',
            field=models.ForeignKey(to='booking.Category', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='end_time',
            field=models.TimeField(null=True, help_text='Please enter in 24 hour format e.g. 21:00', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='location',
            field=models.ForeignKey(to='booking.Location', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='notes_staff',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='notes_user',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='permission',
            field=models.ForeignKey(to='booking.Permission', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='picture',
            field=models.ImageField(blank=True, upload_to='booking', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='start_time',
            field=models.TimeField(null=True, help_text='Please enter in 24 hour format e.g. 19:00', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='title',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
