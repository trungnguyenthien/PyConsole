# Generated by Django 4.2.11 on 2024-05-10 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_logrecord_data_taskrecord_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logrecord',
            name='type',
        ),
    ]