# Generated by Django 5.1 on 2024-08-16 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_import_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='pensioner_list',
            name='csv_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
