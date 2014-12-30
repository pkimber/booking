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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=200)),
                ('promote', models.BooleanField(default=False)),
                ('routine', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Event type',
                'ordering': ('description',),
                'verbose_name_plural': 'Event types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True, null=True)),
                ('url_map', models.URLField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Location',
                'ordering': ('description',),
                'verbose_name_plural': 'Locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Permission',
                'ordering': ('slug',),
                'verbose_name_plural': 'Permissions',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='booking',
            options={'verbose_name': 'Booking', 'ordering': ('from_date', 'from_time'), 'verbose_name_plural': 'Bookings'},
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
            name='from_time',
            field=models.TimeField(help_text='Please enter in 24 hour format e.g. 19:00', blank=True, null=True),
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
            name='to_time',
            field=models.TimeField(help_text='Please enter in 24 hour format e.g. 21:00', blank=True, null=True),
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
            field=models.CharField(blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking',
            name='to_date',
            field=models.DateField(help_text='(dd/mm/yyyy)', blank=True, null=True),
            preserve_default=True,
        ),
    ]
