# Generated by Django 4.2.8 on 2024-03-01 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vitimas", "0007_alter_vitima_status_flag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vitima",
            name="status_flag",
            field=models.CharField(
                blank=True, default="", max_length=200, verbose_name="Status Flag"
            ),
        ),
    ]
