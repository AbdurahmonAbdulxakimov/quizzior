# Generated by Django 3.2.9 on 2024-05-17 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20240506_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='topic',
            new_name='category',
        ),
    ]
