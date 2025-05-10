# load_data.py
import os
import django
import pandas as pd
from django.conf import settings
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MeroVada.settings')
django.setup()

from owner.models import Item

def load_items():
    data = pd.read_csv('items_data.csv')
    User = get_user_model()
    default_owner, _ = User.objects.get_or_create(
        username='admin',
        defaults={'password': 'admin123', 'is_staff': True, 'is_superuser': True}
    )
    
    # Clear existing items (optional)
    Item.objects.all().delete()
    
    for _, row in data.iterrows():
        Item.objects.update_or_create(
            name=row['name'],
            defaults={
                'price': row['price'],
                'location': row['location'],
                'category': row['category'],
                'image': row['image'],
                'owner': default_owner
            }
        )
    print("Data loaded successfully!")

if __name__ == "__main__":
    load_items()