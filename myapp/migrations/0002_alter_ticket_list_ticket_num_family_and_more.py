# Generated by Django 5.1 on 2024-08-20 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_list',
            name='ticket_num_family',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket_list',
            name='ticket_num_ssp',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, unique=True),
        ),
    ]
