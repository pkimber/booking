# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_date', models.DateField(help_text='(dd/mm/yyyy)')),
                ('to_date', models.DateField(help_text='(dd/mm/yyyy)')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Bookings',
                'verbose_name': 'Booking',
                'ordering': ['from_date'],
            },
            bases=(models.Model,),
        ),
    ]
