# Generated by Django 3.2.25 on 2025-07-04 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('Applied', 'Applied'), ('Interview', 'Interview'), ('Offered', 'Offered'), ('Rejected', 'Rejected')], max_length=20),
        ),
    ]
