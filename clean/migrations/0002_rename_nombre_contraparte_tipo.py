# Generated by Django 4.2.6 on 2023-11-02 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clean', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contraparte',
            old_name='nombre',
            new_name='tipo',
        ),
    ]
