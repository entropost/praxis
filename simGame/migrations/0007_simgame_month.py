# Generated by Django 4.2.9 on 2024-05-11 13:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("simGame", "0006_simgame_scenario_alter_company_simgame"),
    ]

    operations = [
        migrations.AddField(
            model_name="simgame",
            name="month",
            field=models.IntegerField(null=True),
        ),
    ]
