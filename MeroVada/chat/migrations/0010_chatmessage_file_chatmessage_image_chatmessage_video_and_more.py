# Generated by Django 5.2 on 2025-05-06 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0009_remove_chatmessage_is_read_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessage",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="chat/files/"),
        ),
        migrations.AddField(
            model_name="chatmessage",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="chat/images/"),
        ),
        migrations.AddField(
            model_name="chatmessage",
            name="video",
            field=models.FileField(blank=True, null=True, upload_to="chat/videos/"),
        ),
        migrations.AlterField(
            model_name="chatmessage",
            name="message",
            field=models.TextField(blank=True, null=True),
        ),
    ]
