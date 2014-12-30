# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20141230_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='end_date',
            field=models.DateField(blank=True, null=True, help_text='(dd/mm/yyyy)'),
            preserve_default=True,
        ),
    ]
