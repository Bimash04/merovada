# Generated by Django 5.2 on 2025-05-06 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0010_chatmessage_file_chatmessage_image_chatmessage_video_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatmessage",
            name="file",
        ),
        migrations.RemoveField(
            model_name="chatmessage",
            name="image",
        ),
        migrations.RemoveField(
            model_name="chatmessage",
            name="video",
        ),
        migrations.AlterField(
            model_name="chatmessage",
            name="message",
            field=models.TextField(),
        ),
    ]
