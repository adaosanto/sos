# Generated by Django 4.2.8 on 2024-03-07 22:45

from django.db import migrations
import stdimage.models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_user_foto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="foto",
            field=stdimage.models.StdImageField(
                default="padrao.jpg",
                force_min_size=False,
                upload_to=users.models.get_file_path,
                variations={"thumb": {"crop": True, "height": 512, "width": 512}},
                verbose_name="Foto",
            ),
        ),
    ]
