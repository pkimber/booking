# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20141230_0219'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('notes_user_staff', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Booking settings',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='booking',
            name='end_date',
            field=models.DateField(help_text='(dd/mm/yyyy)', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking',
            name='notes_staff',
            field=models.TextField(help_text='Notes for members of staff.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking',
            name='notes_user',
            field=models.TextField(help_text='Notes for your users who are logged into the site.', blank=True),
            preserve_default=True,
        ),
    ]
