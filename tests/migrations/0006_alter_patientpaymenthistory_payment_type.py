# Generated by Django 4.2.5 on 2023-10-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_patientpaymenthistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientpaymenthistory',
            name='payment_type',
            field=models.CharField(default='Cash', max_length=50),
        ),
    ]
