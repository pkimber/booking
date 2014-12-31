# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import booking.models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20141230_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='notes',
        ),
        migrations.AddField(
            model_name='bookingsettings',
            name='display_permissions',
            field=models.BooleanField(default=False, help_text='Display permissions on the list of bookings.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='picture',
            field=models.ImageField(blank=True, upload_to='booking', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='title',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='permission',
            field=models.ForeignKey(default=booking.models.default_permission, to='booking.Permission'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='notes_user_staff',
            field=models.BooleanField(default=False, help_text='Allow a member of staff to edit notes for logged in users (and members of staff)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
