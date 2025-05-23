# Generated by Django 4.2.16 on 2025-02-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("renter", "0005_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Completed", "Completed"),
                    ("Cancelled", "Cancelled"),
                ],
                default="Pending",
                max_length=10,
            ),
        ),
    ]
