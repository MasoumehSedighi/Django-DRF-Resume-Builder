# Generated by Django 4.2.15 on 2024-08-25 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='modified_time',
        ),
    ]
