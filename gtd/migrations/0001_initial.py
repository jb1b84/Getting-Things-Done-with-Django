# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=60, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=250)),
                ('completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ranking', models.PositiveIntegerField()),
                ('page', models.ForeignKey(to='gtd.Page')),
            ],
            options={
                'ordering': ['ranking'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('ranking', 'page')]),
        ),
    ]
