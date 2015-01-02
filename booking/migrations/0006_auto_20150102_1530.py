# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20141231_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingsettings',
            name='display_categories',
            field=models.BooleanField(help_text="Does this project use 'Categories'?", default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingsettings',
            name='display_locations',
            field=models.BooleanField(help_text="Does this project use 'Locations'?", default=False),
            preserve_default=True,
        ),
    ]
