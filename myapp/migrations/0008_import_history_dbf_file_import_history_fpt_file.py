# Generated by Django 5.1 on 2024-09-11 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_rename_counter_name_ticket_list_branch_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='import_history',
            name='dbf_file',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='import_history',
            name='fpt_file',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
