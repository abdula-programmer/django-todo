# Generated by Django 4.1.3 on 2022-12-13 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0002_rename_todos_todo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="datecomplited",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
