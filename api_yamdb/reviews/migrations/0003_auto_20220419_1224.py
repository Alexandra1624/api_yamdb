# Generated by Django 2.2.16 on 2022-04-19 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220419_0935'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique review',
        ),
    ]
