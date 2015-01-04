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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('deleted', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(to='booking.Booking')),
            ],
            options={
                'verbose_name_plural': 'Rotas',
                'ordering': ('booking', 'rota__order', 'name'),
                'verbose_name': 'Rota',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RotaType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Rota types',
                'ordering': ('order',),
                'verbose_name': 'Rota type',
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
            field=models.BooleanField(help_text="Does this project use 'Rotas'?", default=False),
            preserve_default=True,
        ),
    ]
