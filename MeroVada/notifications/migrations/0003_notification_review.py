# Generated by Django 4.2.16 on 2025-01-26 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0002_review_is_approved"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="review",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="notifications.review",
            ),
        ),
    ]
