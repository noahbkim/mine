# Generated by Django 2.1.4 on 2019-01-01 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190101_1843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='means',
            new_name='type',
        ),
    ]