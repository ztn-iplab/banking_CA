# Generated by Django 5.0.4 on 2025-03-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logger", "0005_backspacecount_user_keystrokelog_session_duration_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="backspacecount",
            name="timestamp",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="keystrokelog",
            name="timestamp",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="mouseactionlog",
            name="timestamp",
            field=models.DateTimeField(),
        ),
    ]
