from django import forms
from .models import Item,ItemImage
from django.forms import inlineformset_factory
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'category', 'location', 'image', 'video', 'description']
# Allow 1-20 images, enforce at least 1
ItemImageFormSet = inlineformset_factory(
    Item,
    ItemImage,
    fields=('image',),
    extra=9,
    min_num=1,
    max_num=10,
    validate_min=True,
)

