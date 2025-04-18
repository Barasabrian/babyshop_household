from django import forms
from .models import HouseholdProduct

class HouseholdProductForm(forms.ModelForm):
    class Meta:
        model = HouseholdProduct
        fields = ['category', 'name', 'slug', 'price', 'description', 
                 'material', 'dimensions', 'stock', 'image', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False