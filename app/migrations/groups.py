from django.db import models, migrations


def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    admin_group, _ = Group.objects.get_or_create(name='Admin')
    painel_group, _ = Group.objects.get_or_create(name='Painel de Recebimento')
    # permissions_to_add_admin = ['Can add User', 'Can change User', 'Can view User', 'Can add Vitima', 'Can change vitima', 'Can view Vitima']
    # permissions_admin = [Permission.objects.get(name=permission_add) for permission_add in permissions_to_add_admin]
    # for permission_admin in permissions_admin:
    #     admin_group.permissions.add(permission_admin)
        
def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=[
            u'Admin',
            u'Painel de Recebimento',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__latest__'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]