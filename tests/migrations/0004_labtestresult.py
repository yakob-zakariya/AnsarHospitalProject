# Generated by Django 4.2.5 on 2023-10-10 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('tests', '0003_alter_vitalregistration_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('result_comment', models.TextField()),
                ('result_date', models.DateTimeField(auto_now_add=True)),
                ('lab_technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.labtecnician')),
                ('labtestorder', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tests.labtestorder')),
            ],
            options={
                'db_table': 'LabTestResult',
            },
        ),
    ]