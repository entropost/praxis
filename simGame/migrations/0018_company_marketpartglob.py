# Generated by Django 4.2.9 on 2024-06-08 13:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("simGame", "0017_rename_marketparp2_company_marketpartp2"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="marketPartGlob",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
    ]
