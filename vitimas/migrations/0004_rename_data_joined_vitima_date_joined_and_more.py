# Generated by Django 4.2.8 on 2024-02-28 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "vitimas",
            "0003_vitima_access_key_vitima_is_admin_vitima_last_login_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="vitima",
            old_name="data_joined",
            new_name="date_joined",
        ),
        migrations.RemoveField(
            model_name="vitima",
            name="chave_acesso",
        ),
    ]
