# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20150104_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingsettings',
            name='edit_from_detail',
            field=models.BooleanField(help_text='Edit events from the detail page.', default=False),
            preserve_default=True,
        ),
    ]
