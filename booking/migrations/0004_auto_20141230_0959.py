# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def _init_state(model, slug, description):
    try:
        model.objects.get(slug=slug)
    except model.DoesNotExist:
        instance = model(**dict(slug=slug, description=description))
        instance.save()
        instance.full_clean()


def default_state(apps, schema_editor):
    Permission = apps.get_model('booking', 'Permission')
    _init_state(Permission, 'public', 'Public')
    _init_state(Permission, 'staff', 'Staff only')
    _init_state(Permission, 'user', 'User')


class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0003_auto_20141230_0350'),
    ]
    operations = [
        migrations.RunPython(default_state),
    ]
