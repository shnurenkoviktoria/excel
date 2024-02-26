# Generated by Django 4.2.5 on 2023-10-04 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sheet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sheet_id", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Cell",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cell_id", models.CharField(max_length=100)),
                ("value", models.CharField(max_length=100, null=True)),
                ("result", models.CharField(max_length=100, null=True)),
                (
                    "sheet_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="excel.sheet"
                    ),
                ),
            ],
        ),
    ]
