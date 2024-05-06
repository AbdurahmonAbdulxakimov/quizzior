# Generated by Django 3.2.9 on 2024-05-06 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_rename_correct_answers_userquizstatistic_user_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquizstatistic',
            name='correct_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userquizstatistic',
            name='wrong_answers',
            field=models.IntegerField(default=0),
        ),
    ]