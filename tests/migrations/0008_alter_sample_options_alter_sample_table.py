# Generated by Django 4.2.5 on 2023-10-12 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0007_sample'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sample',
            options={'ordering': ['-date_sample_taken']},
        ),
        migrations.AlterModelTable(
            name='sample',
            table='Sample',
        ),
    ]
