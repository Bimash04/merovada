import random
import os
from django.core.files import File
from owner.models import Item
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

LOCATIONS = ['Kathmandu', 'Biratnagar', 'Letang']
CATEGORIES = ['Room', 'Apartment', 'Flat', 'Furniture', 'Bike', 'Car', 'Other']

ITEM_NAMES = {
    'Room': ['Single Room', 'Deluxe Room', 'Suite'],
    'Apartment': ['Studio Apartment', '2BHK Apartment', '3BHK Apartment'],
    'Flat': ['Ground Floor Flat', 'Penthouse'],
    'Furniture': ['Sofa Set', 'Dining Table', 'Bed'],
    'Bike': ['Scooter', 'Sports Bike', 'Cruiser Bike'],
    'Car': ['Sedan', 'SUV', 'Hatchback'],
    'Other': ['Miscellaneous Item']
}

# Sample images stored in 'media/sample_images'
SAMPLE_IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, 'item_images')
SAMPLE_IMAGES = [os.path.join(SAMPLE_IMAGE_DIR, img) for img in os.listdir(SAMPLE_IMAGE_DIR) if img.endswith(('.jpg', '.png'))]

def generate_items(n=50):
    users = list(User.objects.all())
    if not users:
        print("No users found. Create at least one user first.")
        return

    if not SAMPLE_IMAGES:
        print("No sample images found in 'media/sample_images'. Add some images first.")
        return

    for _ in range(n):
        category = random.choice(CATEGORIES)
        name = random.choice(ITEM_NAMES[category])
        location = random.choice(LOCATIONS)
        price = round(random.uniform(1000, 50000), 2)
        owner = random.choice(users)
        image_path = random.choice(SAMPLE_IMAGES)

        item = Item(
            name=name, description=f"A great {name} available in {location}.",
            price=price, category=category, location=location, owner=owner
        )

        with open(image_path, 'rb') as img_file:
            item.image.save(os.path.basename(image_path), File(img_file), save=True)

    print(f"{n} items added successfully!")

# Run this in Django shell:
# python manage.py shell
# >>> from owner.data_generator import generate_items
# >>> generate_items()
