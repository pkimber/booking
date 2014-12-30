# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import booking.models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20141230_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='permission',
            field=models.ForeignKey(to='booking.Permission', default=booking.models.default_permission),
            preserve_default=True,
        ),
    ]
