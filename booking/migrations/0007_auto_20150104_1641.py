# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20150102_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('deleted', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(to='booking.Booking')),
            ],
            options={
                'verbose_name': 'Rota',
                'verbose_name_plural': 'Rotas',
                'ordering': ('booking', 'rota__order', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RotaType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Rota type',
                'verbose_name_plural': 'Rota types',
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rota',
            name='rota',
            field=models.ForeignKey(to='booking.RotaType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingsettings',
            name='display_rota',
            field=models.BooleanField(default=False, help_text="Does this project use 'Rotas'?"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingsettings',
            name='pdf_heading',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
