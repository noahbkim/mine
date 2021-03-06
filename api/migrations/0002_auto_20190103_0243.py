# Generated by Django 2.1.4 on 2019-01-03 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='api.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='details',
            field=models.ManyToManyField(blank=True, null=True, related_name='items', to='api.Detail'),
        ),
        migrations.AlterField(
            model_name='list',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, related_name='lists', through='api.ListInventory', to='api.Item'),
        ),
        migrations.AlterField(
            model_name='location',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, related_name='locations', through='api.LocationInventory', to='api.Item'),
        ),
    ]
