# Generated by Django 5.1 on 2024-09-10 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_import_history_branch_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket_list',
            old_name='counter_name',
            new_name='branch_name',
        ),
    ]
