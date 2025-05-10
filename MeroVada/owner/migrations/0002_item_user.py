from django.db import migrations
from django.conf import settings

def populate_item_user(apps, schema_editor):
    Item = apps.get_model('owner', 'Item')
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])  # Dynamically get the custom user model

    # Assign a default user to items with no user
    default_user = User.objects.first()  # Replace with your logic to get a default user
    if default_user:  # Ensure a default user exists
        for item in Item.objects.filter(user__isnull=True):
            item.user = default_user
            item.save()

class Migration(migrations.Migration):
    dependencies = [
        ('owner', '0001_initial'),  # Replace with the correct migration dependency
    ]

    operations = [
        migrations.RunPython(populate_item_user),
    ]
