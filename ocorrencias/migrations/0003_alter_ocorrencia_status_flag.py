# Generated by Django 4.2.8 on 2024-02-29 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ocorrencias", "0002_ocorrencia_status_flag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ocorrencia",
            name="status_flag",
            field=models.CharField(
                blank="", max_length=200, null=True, verbose_name="Status Flag"
            ),
        ),
    ]
