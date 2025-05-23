# Generated by Django 4.2.16 on 2025-02-06 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0002_remove_chatroom_participants_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatmessage",
            name="message",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="chatmessage",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="received_messages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
